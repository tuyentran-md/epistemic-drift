"""
Generation pipeline for OSF X4RP5 (https://doi.org/10.17605/OSF.IO/X4RP5).

- Primary arm (confirmatory): 12 topics × 30 reps × 3 models = 1080 abstracts.
- Sensitivity arm (exploratory): 4 topics × 30 reps × 3 models × 2 alt prompts = 720 abstracts.
- Human comparators (Europe PMC): ~10 abstracts × 12 topics ≈ 120.

Each AI generation = independent API call (fresh context per call).
Crucial: NOT a single prompt asking for 30 abstracts (that would condition outputs on each other).

Canonical-prompt hash check runs at start, midway, and end of each generation batch
(stability metric per OSF prereg §7).

Examples:
    python 02_generation/generate.py --mode ai --prompt primary
    python 02_generation/generate.py --mode ai --prompt alt_1 --topics T03,T05,T10,T12
    python 02_generation/generate.py --mode ai --prompt alt_2 --topics T03,T05,T10,T12
    python 02_generation/generate.py --mode human
"""

import argparse
import itertools
import json
import os
import re
import string
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import urllib.parse
import urllib.request

from google import genai
from google.genai import types
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"
load_dotenv(ROOT / ".env")

GOOGLE_KEYS = [os.environ.get("GOOGLE_API_KEY")]
for i in range(2, 16):  # supports up to GOOGLE_API_KEY_15
    k = os.environ.get(f"GOOGLE_API_KEY_{i}")
    if k:
        GOOGLE_KEYS.append(k)
GOOGLE_KEYS = [k for k in GOOGLE_KEYS if k]

EUROPEPMC_BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest"
OLLAMA_BASE = os.environ.get("OLLAMA_BASE", "http://localhost:11434")

BACKEND = os.environ.get("GEN_BACKEND", "gemini")
GENERATOR_MODEL = os.environ.get("GEN_MODEL", "gemini-3-pro-preview")
TEMPERATURE = 0.7
TOP_P = 1.0
MAX_OUTPUT_TOKENS = 8000
N_SAMPLES_PER_TOPIC = 30
MAX_HUMAN_PER_TOPIC = 10
MAX_WORKERS = 3
CANONICAL_TEMP = 0.0
CANONICAL_MAX_TOKENS = 80
JACCARD_THRESHOLD = 0.85

_gemini_clients = []
_gemini_cycle = None


def _get_gemini_client():
    """Round-robin across GOOGLE_API_KEY{,_2,_3}."""
    global _gemini_clients, _gemini_cycle
    if not _gemini_clients:
        if not GOOGLE_KEYS:
            sys.exit("ERROR: no GOOGLE_API_KEY{,_2,_3} present in .env (required for backend=gemini)")
        _gemini_clients = [genai.Client(api_key=k) for k in GOOGLE_KEYS]
        _gemini_cycle = itertools.cycle(_gemini_clients)
    return next(_gemini_cycle)


def load_topics():
    with open(ROOT / "01_topics" / "topics.json") as f:
        return json.load(f)["topics"]


def load_prompt_template(prompt_id):
    path = PROMPTS_DIR / f"{prompt_id}.txt"
    if not path.exists():
        sys.exit(f"ERROR: prompt template not found: {path}")
    return path.read_text()


def render_prompt(template, topic):
    return (template
            .replace("[TOPIC_TITLE]", topic["topic_title"])
            .replace("[P]", topic["P"])
            .replace("[I]", topic["I"])
            .replace("[C]", topic["C"])
            .replace("[O]", topic["O"]))


def _generate_gemini(prompt, temperature=TEMPERATURE, max_tokens=MAX_OUTPUT_TOKENS):
    response = _get_gemini_client().models.generate_content(
        model=GENERATOR_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=temperature,
            top_p=TOP_P,
            max_output_tokens=max_tokens,
        ),
    )
    return (response.text or "").strip()


def _generate_ollama(prompt, temperature=TEMPERATURE, max_tokens=600):
    payload = {
        "model": GENERATOR_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": temperature, "top_p": TOP_P, "num_predict": max_tokens},
    }
    req = urllib.request.Request(
        f"{OLLAMA_BASE}/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=300) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return (data.get("response") or "").strip()


def _generate(prompt, **kwargs):
    if BACKEND == "gemini":
        return _generate_gemini(prompt, **kwargs)
    if BACKEND == "ollama":
        return _generate_ollama(prompt, **kwargs)
    raise ValueError(f"Unknown BACKEND: {BACKEND}")


def generate_one(topic, sample_id, prompt_template, prompt_id):
    prompt = render_prompt(prompt_template, topic)
    try:
        text = _generate(prompt)
        return {
            "topic_id": topic["id"],
            "specialty": topic["specialty"],
            "sample_id": sample_id,
            "prompt_id": prompt_id,
            "prompt": prompt,
            "abstract": text if text else None,
            "model": GENERATOR_MODEL,
            "backend": BACKEND,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "timestamp": time.time(),
            "error": None if text else "empty_response",
        }
    except Exception as e:
        return {
            "topic_id": topic["id"],
            "specialty": topic["specialty"],
            "sample_id": sample_id,
            "prompt_id": prompt_id,
            "prompt": prompt,
            "abstract": None,
            "model": GENERATOR_MODEL,
            "backend": BACKEND,
            "temperature": TEMPERATURE,
            "top_p": TOP_P,
            "timestamp": time.time(),
            "error": str(e),
        }


def _model_slug():
    return GENERATOR_MODEL.replace("/", "_").replace(":", "_")


def _tokenize_for_jaccard(text, max_tokens=200):
    """Whitespace + punctuation split, lowercase, take first max_tokens."""
    text = text.lower()
    text = re.sub(rf"[{re.escape(string.punctuation)}]", " ", text)
    toks = text.split()
    return toks[:max_tokens]


def _jaccard(a, b):
    A, B = set(a), set(b)
    if not A and not B:
        return 1.0
    return len(A & B) / max(1, len(A | B))


def run_canonical_check(label, batch_id):
    canonical = load_prompt_template("canonical")
    t0 = time.time()
    try:
        text = _generate(canonical, temperature=CANONICAL_TEMP, max_tokens=CANONICAL_MAX_TOKENS)
    except Exception as e:
        text = f"ERROR: {e}"
    return {
        "batch_id": batch_id,
        "checkpoint": label,
        "model": GENERATOR_MODEL,
        "backend": BACKEND,
        "timestamp": t0,
        "output": text,
    }


def append_canonical_log(entries):
    log_path = ROOT / "logs" / "canonical_hash_log.csv"
    log_path.parent.mkdir(exist_ok=True)
    df_new = pd.DataFrame(entries)
    if log_path.exists():
        df_old = pd.read_csv(log_path)
        df = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df = df_new
    df.to_csv(log_path, index=False)


def evaluate_canonical_pairs(start_out, mid_out, end_out):
    pairs = [
        ("start_mid", start_out, mid_out),
        ("mid_end", mid_out, end_out),
        ("start_end", start_out, end_out),
    ]
    rows = []
    flagged = False
    for name, a, b in pairs:
        ta = _tokenize_for_jaccard(a)
        tb = _tokenize_for_jaccard(b)
        j = _jaccard(ta, tb)
        ok = j >= JACCARD_THRESHOLD
        if not ok:
            flagged = True
        rows.append({"pair": name, "jaccard": j, "passes_0.85": ok})
    return rows, flagged


def generate_ai_abstracts(prompt_id, topic_filter=None):
    topics = load_topics()
    if topic_filter:
        wanted = set(topic_filter)
        topics = [t for t in topics if t["id"] in wanted]
        if not topics:
            sys.exit(f"ERROR: no topics matched filter {topic_filter}")
        print(f"[AI] Topic filter applied → {len(topics)} topics: {[t['id'] for t in topics]}")

    prompt_template = load_prompt_template(prompt_id)
    slug = _model_slug()
    suffix = "" if prompt_id == "primary" else f"__{prompt_id}"
    out_path = ROOT / "03_data" / f"ai_abstracts__{slug}{suffix}.csv"
    jsonl_path = ROOT / "03_data" / f"ai_abstracts__{slug}{suffix}.jsonl"
    out_path.parent.mkdir(exist_ok=True)

    done = set()
    if jsonl_path.exists():
        with open(jsonl_path) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["topic_id"], r["sample_id"]))
                except Exception:
                    continue

    jobs = [(t, sid) for t in topics for sid in range(N_SAMPLES_PER_TOPIC) if (t["id"], sid) not in done]
    total = len(topics) * N_SAMPLES_PER_TOPIC
    if not jobs:
        print(f"[AI] All {total} jobs already done in {jsonl_path}")
        return

    batch_id = f"{slug}__{prompt_id}__{int(time.time())}"
    print(f"[AI] Batch {batch_id}: {len(jobs)}/{total} abstracts (already done: {len(done)})")

    canonical_entries = [run_canonical_check("start", batch_id)]
    midway_index = max(1, len(jobs) // 2)
    mid_done = False

    with open(jsonl_path, "a") as fout:
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            futures = {pool.submit(generate_one, t, sid, prompt_template, prompt_id): (t, sid)
                       for (t, sid) in jobs}
            done_count = 0
            for fut in tqdm(as_completed(futures), total=len(jobs), desc=f"AI gen {prompt_id}"):
                r = fut.result()
                fout.write(json.dumps(r) + "\n")
                fout.flush()
                done_count += 1
                if not mid_done and done_count >= midway_index:
                    canonical_entries.append(run_canonical_check("mid", batch_id))
                    mid_done = True

    canonical_entries.append(run_canonical_check("end", batch_id))

    if len(canonical_entries) >= 3:
        pair_rows, flagged = evaluate_canonical_pairs(
            canonical_entries[0]["output"],
            canonical_entries[1]["output"],
            canonical_entries[2]["output"],
        )
    else:
        pair_rows, flagged = [], False
    for c in canonical_entries:
        c["batch_flagged"] = flagged
    append_canonical_log(canonical_entries)

    print(f"[Canonical-hash] batch {batch_id}:")
    for r in pair_rows:
        print(f"  {r['pair']}: J={r['jaccard']:.3f} {'PASS' if r['passes_0.85'] else 'FLAG'}")
    if flagged:
        print(f"[Canonical-hash] BATCH FLAGGED — review canonical_hash_log.csv and consider re-run.")

    rows = []
    with open(jsonl_path) as f:
        for line in f:
            rows.append(json.loads(line))
    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)
    n_ok = df["error"].isna().sum() if "error" in df else len(df)
    n_err = df["error"].notna().sum() if "error" in df else 0
    print(f"[AI] Done. Saved {len(df)} rows to {out_path} ({n_ok} ok, {n_err} errors)")


# ───── Human comparator pull (Europe PMC) ────────────────────────────────────
def _http_get(url, retries=2):
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=20) as resp:
                return resp.read().decode("utf-8", errors="replace")
        except Exception:
            if attempt < retries:
                time.sleep(1)
            else:
                raise


def pull_human_for_topic(topic):
    query = topic["pubmed_query"]
    try:
        params = urllib.parse.urlencode({
            "query": query,
            "format": "json",
            "pageSize": "50",
            "resultType": "core",
        })
        url = f"{EUROPEPMC_BASE}/search?{params}"
        body = _http_get(url)
        data = json.loads(body)
        results = (data.get("resultList") or {}).get("result", [])
        if not results:
            return []

        seen_authors = set()
        out = []
        for art in results:
            try:
                abstract_text = art.get("abstractText", "") or ""
                if len(abstract_text) < 200:
                    continue
                authors_str = art.get("authorString", "")
                first_author = authors_str.split(",")[0].strip() if authors_str else "Unknown"
                if first_author in seen_authors:
                    continue
                seen_authors.add(first_author)

                pub_types_raw = (art.get("pubTypeList") or {}).get("pubType", [])
                if isinstance(pub_types_raw, list):
                    pub_type = ",".join(str(t) for t in pub_types_raw if t)
                else:
                    pub_type = str(pub_types_raw)
                pt_lower = pub_type.lower()
                if any(k in pt_lower for k in ["letter", "editorial", "comment", "news", "biography"]):
                    continue
                if not any(k in pt_lower for k in ["journal article", "research", "review", "trial",
                                                     "meta-analysis", "randomi"]):
                    continue

                out.append({
                    "topic_id": topic["id"],
                    "specialty": topic["specialty"],
                    "pmid": art.get("pmid", "") or art.get("id", ""),
                    "first_author": first_author,
                    "year": str(art.get("pubYear", "")),
                    "title": art.get("title", "") or "",
                    "abstract": abstract_text,
                })
                if len(out) >= MAX_HUMAN_PER_TOPIC:
                    break
            except Exception:
                continue
        return out
    except Exception as e:
        print(f"[Human] Error for topic {topic['id']}: {type(e).__name__}: {e}")
        return []


def pull_human_abstracts():
    topics = load_topics()
    out_path = ROOT / "03_data" / "human_abstracts.csv"
    out_path.parent.mkdir(exist_ok=True)
    print(f"[Human] Pulling abstracts for {len(topics)} topics via Europe PMC...")
    rows = []
    for t in tqdm(topics, desc="Europe PMC pull"):
        rows.extend(pull_human_for_topic(t))
        time.sleep(0.4)
    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)
    if len(df) == 0:
        print("[Human] WARNING: 0 abstracts. Check queries.")
    else:
        print(f"[Human] Done. Saved {len(df)} abstracts across {df['topic_id'].nunique()} topics → {out_path}")
        print(df.groupby("topic_id").size().to_string())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["ai", "human", "all"], default="all")
    ap.add_argument("--prompt", choices=["primary", "alt_1", "alt_2"], default="primary",
                    help="Generation prompt template (only meaningful for --mode ai)")
    ap.add_argument("--topics", default=None,
                    help="Comma-separated topic IDs to limit (e.g. 'T03,T05,T10,T12')")
    ap.add_argument("--n", type=int, default=None, help="Override N_SAMPLES_PER_TOPIC")
    ap.add_argument("--test", action="store_true", help="N=1 per topic for smoke test")
    args = ap.parse_args()

    global N_SAMPLES_PER_TOPIC
    if args.test:
        N_SAMPLES_PER_TOPIC = 1
        print("[TEST MODE] N_SAMPLES_PER_TOPIC = 1")
    elif args.n:
        N_SAMPLES_PER_TOPIC = args.n
        print(f"[OVERRIDE] N_SAMPLES_PER_TOPIC = {args.n}")

    topic_filter = None
    if args.topics:
        topic_filter = [t.strip() for t in args.topics.split(",") if t.strip()]

    if args.mode in ("ai", "all"):
        generate_ai_abstracts(args.prompt, topic_filter=topic_filter)
    if args.mode in ("human", "all"):
        pull_human_abstracts()


if __name__ == "__main__":
    main()

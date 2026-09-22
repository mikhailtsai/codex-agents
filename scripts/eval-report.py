#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".codex-evals/runs.jsonl"
VALID = {"PASS","FAIL","HUMAN_CORRECTION","REGRESSION"}

rows=[]
errors=[]
if PATH.exists():
    for n,line in enumerate(PATH.read_text().splitlines(),1):
        if not line.strip(): continue
        try: row=json.loads(line)
        except Exception as e:
            errors.append(f"line {n}: invalid JSON: {e}"); continue
        if row.get("outcome") not in VALID:
            errors.append(f"line {n}: invalid outcome {row.get('outcome')!r}")
        if not isinstance(row.get("agents",[]),list):
            errors.append(f"line {n}: agents must be a list")
        if not isinstance(row.get("retries",0),int) or row.get("retries",0)<0:
            errors.append(f"line {n}: retries must be a non-negative integer")
        rows.append(row)

if errors:
    print("Eval journal FAILED")
    for e in errors: print("-",e)
    sys.exit(1)

n=len(rows)
print(f"Tasks: {n}")
if not n:
    print("No outcomes recorded yet.")
    sys.exit(0)

out=Counter(r["outcome"] for r in rows)
for k in ["PASS","FAIL","HUMAN_CORRECTION","REGRESSION"]:
    print(f"{k}: {out[k]} ({out[k]/n:.1%})")
print(f"Average retries: {sum(r.get('retries',0) for r in rows)/n:.2f}")
print(f"Terra escalations: {sum(bool(r.get('terra')) for r in rows)} ({sum(bool(r.get('terra')) for r in rows)/n:.1%})")
print(f"Sol escalations: {sum(bool(r.get('sol')) for r in rows)} ({sum(bool(r.get('sol')) for r in rows)/n:.1%})")
print(f"Human correction flag: {sum(bool(r.get('human_correction')) for r in rows)} ({sum(bool(r.get('human_correction')) for r in rows)/n:.1%})")
agents=Counter(a for r in rows for a in r.get("agents",[]))
if agents:
    print("Agent usage:")
    for a,c in agents.most_common(): print(f"  {a}: {c}")
cats=Counter(r.get("category","unknown") for r in rows)
if cats:
    print("Categories:")
    for a,c in cats.most_common(): print(f"  {a}: {c}")

#!/usr/bin/env python3
from collections import Counter
from pathlib import Path
import json
import sys

try:
    from eval_schema import validate_row
except ImportError as error:
    print("Eval journal FAILED")
    print(f"- scripts/eval_schema.py: cannot import shared schema: {error}")
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / ".codex-evals/runs.jsonl"
AGENTS_PATH = ROOT / ".codex/agents"
allowed_agents = {path.stem for path in AGENTS_PATH.glob("*.toml")}
rows=[]
errors=[]
if not PATH.is_file():
    errors.append(".codex-evals/runs.jsonl: missing evaluation journal")
else:
    for n,line in enumerate(PATH.read_text().splitlines(),1):
        if not line.strip(): continue
        try: row=json.loads(line)
        except Exception as e:
            errors.append(f"line {n}: invalid JSON: {e}"); continue
        errors.extend(validate_row(row, n, allowed_agents))
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
checks_passed = sum(r.get("checks", {}).get("passed", 0) for r in rows)
checks_failed = sum(r.get("checks", {}).get("failed", 0) for r in rows)
review_findings = sum(r.get("review_findings", 0) for r in rows)
print(f"Checks passed: {checks_passed}")
print(f"Checks failed: {checks_failed}")
print(f"Review findings: {review_findings}")
agents=Counter(a for r in rows for a in r.get("agents",[]))
if agents:
    print("Agent usage:")
    for a,c in agents.most_common(): print(f"  {a}: {c}")
cats=Counter(r.get("category","unknown") for r in rows)
if cats:
    print("Categories:")
    for a,c in cats.most_common(): print(f"  {a}: {c}")

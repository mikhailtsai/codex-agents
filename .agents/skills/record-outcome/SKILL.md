---
name: record-outcome
description: Record a compact non-sensitive outcome after substantial work so the harness can be evaluated from real tasks.
---

# Record outcome

After substantial work, append one JSON object to `.codex-evals/runs.jsonl`.

Record:
- UTC timestamp
- short non-sensitive task label and category
- outcome: PASS, FAIL, HUMAN_CORRECTION, or REGRESSION
- agents actually used
- retry count
- deterministic checks passed/failed
- meaningful review findings
- whether Terra or Sol was used
- whether a human correction was required
- short non-sensitive notes/tags when useful

Do not store prompts, code, secrets, credentials, personal data, raw logs, or large tool outputs.

PASS means available validation found no known defect; it is not a claim of mathematical correctness.
If a user later reports a defect after completion, append a HUMAN_CORRECTION or REGRESSION record rather than rewriting history.

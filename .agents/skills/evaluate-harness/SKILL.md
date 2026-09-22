---
name: evaluate-harness
description: Analyze accumulated task outcomes and deterministic metrics to find recurring workflow weaknesses and evidence-backed harness improvements.
---

# Evaluate harness

1. Run `python scripts/eval-report.py` first. Treat its output as measured evidence.
2. Inspect relevant records in `.codex-evals/runs.jsonl`, especially FAIL, HUMAN_CORRECTION, REGRESSION, repeated retries, and expensive escalations.
3. Look for repeated failure classes, not isolated anecdotes.
4. Separate measured facts from hypotheses.
5. Recommend the smallest durable improvement: test/check, repository knowledge, debugging aid, observability, skill, routing change, or only when truly necessary a new role.
6. Use `improve-harness` for an approved concrete improvement.
7. Do not optimize metrics by weakening validation or avoiding difficult tasks.
8. Do not infer model quality from tiny samples. State sample size and uncertainty.

Prefer Luna for this analysis. Terra/Sol are unnecessary unless the analysis exposes an independently consequential architecture problem.

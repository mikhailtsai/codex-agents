---
name: plan
description: Create an execution plan for complex or risky work using repository evidence; use when implementation needs multiple coordinated steps or durable decisions.
---

# Execution plan

Use a lightweight in-context plan for small work. For complex/risky work create `docs/exec-plans/active/<slug>.md`.

A durable plan should contain only:
- goal and acceptance criteria
- verified current-state evidence
- scope / non-goals
- ordered implementation slices
- validation for each risky slice
- decisions and unresolved questions
- progress log

Delegate product/system/code investigation to Luna agents where useful. Parallelize independent investigation.
Do not use Terra unless Luna findings expose a consequential unresolved architecture decision.
Do not use Sol unless Terra or repeated Luna attempts still cannot resolve a high-impact blocker.

Update the plan as facts change. Move completed durable plans to `docs/exec-plans/completed/`.

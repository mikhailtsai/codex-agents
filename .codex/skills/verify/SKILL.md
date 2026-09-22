---
name: verify
description: Prove a change works with deterministic checks and focused behavioral evidence; use before declaring substantial work complete.
---

# Verify

1. Derive validation from the actual changed behavior and acceptance criteria.
2. Prefer repository-provided deterministic commands: tests, typecheck, lint, build, structural checks.
3. Run narrow checks while iterating; run the relevant full gate before handoff when practical.
4. Use the Luna test-engineer for independent behavioral/regression coverage on non-trivial changes.
5. Never report a check as passing unless it actually ran.
6. Record failures accurately; distinguish pre-existing failures from regressions only with evidence.
7. If a failure repeats without new evidence, stop looping and escalate the unresolved question.

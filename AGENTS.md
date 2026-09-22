# Codex agent workflow

Use Codex itself as the runtime. This repository adds only a project-local workflow layer.
The project config defaults the primary session and spawned agents to `gpt-5.6-luna` with medium reasoning. An explicit CLI `--model` selection may override that default; do not escalate by habit.

## Default policy

Luna first. The primary session may itself be Luna. Use Luna agents for almost all analysis, implementation, testing, and review.

Escalation is exceptional:
- `architect` (Terra): consequential architecture decisions, conflicting evidence, or repeated Luna failure.
- `oracle` (Sol): only when Terra still cannot resolve a high-impact blocker.
- Astra is not part of the normal workflow. If explicitly selected, keep routine work delegated to Luna.

## Map

- Existing project docs remain authoritative.
- `docs/agent/` contains only missing agent-facing maps and links.
- `docs/exec-plans/` contains durable plans for complex work.
- `.agents/skills/` contains reusable procedures.
- `.codex-evals/` contains compact non-sensitive outcomes from real tasks; it is evidence for improving this workflow, not raw telemetry.

Run `bootstrap-project` when architecture, workflows, validation, or product rules are not legible.

## Luna team

- `product-analyst`: requirements, business rules, acceptance criteria, edge cases.
- `system-analyst`: end-to-end workflows, state/data flow, integrations and boundaries.
- `researcher`: focused technical/code investigation.
- `implementer`: bounded implementation.
- `worker`: mechanical edits, commands, diagnostics and narrow fixes.
- `test-engineer`: behavioral/regression tests and validation.
- `reviewer`: correctness, regression, contracts and architecture review.
- `requirements-reviewer`: acceptance against the original request.
- `security-reviewer`: security-sensitive changed surfaces only.

## Routing

Use the smallest team that gives high confidence. Never run every role mechanically.

- tiny/mechanical → direct work or `worker`
- bug/failure → `debug` when root cause is unknown; otherwise `researcher` if needed → `implementer` → `verify`
- ambiguous feature → add `product-analyst`
- unclear cross-system flow → add `system-analyst`
- substantial/risky change → `verify` + selected `review-loop`
- repeated failure or illegible environment → `improve-harness`
- periodically or after enough real tasks → `evaluate-harness`
- complex multi-step work → `plan`

Parallelize independent investigation and reviews.

## Handoffs

A delegation includes exact goal, scope, known evidence, expected output, and validation. Pass prior findings forward; do not make agents rediscover context. Distinguish evidence from inference and escalate ambiguity instead of inventing decisions.
Ask Codex to delegate explicitly when parallel work is useful, for example: "Use `researcher` to map the affected path, then have `implementer` make the bounded change and `reviewer` inspect the diff." Keep each handoff narrow and ask for a compact summary with paths and validation results.

## Completion

For substantial work:
1. establish only missing requirements/system/code context;
2. implement in bounded slices;
3. run deterministic project checks;
4. run risk-selected independent reviews;
5. correct concrete findings;
6. re-run invalidated checks/reviews;
7. stop when evidence is clean;
8. for substantial work, use `record-outcome` to append a compact result to `.codex-evals/runs.jsonl`.

Never claim a check ran when it did not. Reviewer PASS does not replace deterministic validation.

Do not spawn agents for tiny mechanical changes or independent work that cannot benefit from parallelism. Every extra thread consumes tokens and context; prefer one focused Luna agent over a broad panel.

## Repository improvement

When the same failure recurs, do not grow this file. Improve the repository: tool, test, linter, structural check, observability, documentation, or discoverability. Prefer enforceable invariants over prompt rules.

Keep this file a map, not a manual.


## Evaluation

Do not rely on agent self-confidence as evidence. Prefer deterministic checks, independent review, real user corrections, regressions, and accumulated outcomes. Periodically run `evaluate-harness`; improve recurring failure classes rather than reacting to isolated anecdotes. Never store prompts, secrets, source code, personal data, or raw telemetry in the eval journal.

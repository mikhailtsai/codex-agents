# Codex agent workflow

Use Codex itself as the runtime. This repository only adds a project-local workflow layer.

## Default policy

**Luna first.** The primary session may itself be Luna. Use Luna agents for almost all analysis, implementation, testing, and review.

Escalation is exceptional:
- `architect` (Terra): consequential architecture decisions, unresolved conflicting evidence, or repeated Luna failure.
- `oracle` (Sol): only when Terra still cannot resolve a high-impact blocker.
- Do not use Astra as part of the normal workflow. If the user explicitly chooses Astra, treat it as a scarce escalation resource and still delegate routine work to Luna.

## Map

Repository knowledge should be discoverable progressively:
- existing project docs remain authoritative;
- `docs/agent/` contains only missing agent-facing maps and links;
- `docs/exec-plans/` contains durable plans for complex work;
- `.codex/skills/` contains reusable procedures.

Run `bootstrap-project` when adopting this workflow in a repository whose architecture, workflows, validation, or product rules are not legible.

## Luna team

- `product-analyst`: requirements, business rules, acceptance criteria, edge cases.
- `system-analyst`: end-to-end workflows, state/data flow, integrations and boundaries.
- `researcher`: focused technical/code investigation.
- `implementer`: bounded implementation.
- `worker`: mechanical edits, commands, diagnostics and narrow fixes.
- `test-engineer`: behavioral/regression tests and validation.
- `reviewer`: correctness, regression, contracts and architecture review.
- `requirements-reviewer`: acceptance against the original request.
- `security-reviewer`: only for security-sensitive changed surfaces.

## Routing

Use the smallest team that gives high confidence. Never run every role mechanically.

- tiny/mechanical → direct work or `worker`
- clear bug/change → `researcher` if needed → `implementer` → `verify`
- ambiguous feature → add `product-analyst`
- unclear cross-system flow → add `system-analyst`
- substantial/risky change → `verify` + selected `review-loop`
- repeated failure/illegible environment → `improve-harness`
- complex multi-step work → `plan`

Parallelize independent investigation and reviews.

## Handoffs

A delegation includes the exact goal, scope, known evidence, expected output, and validation. Pass prior findings forward; do not make agents rediscover context.

Agents distinguish evidence from inference and escalate ambiguity instead of inventing decisions.

## Completion

For substantial work:
1. establish only the missing requirements/system/code context;
2. implement in bounded slices;
3. run deterministic project checks;
4. run risk-selected independent reviews;
5. correct concrete findings;
6. re-run invalidated checks/reviews;
7. stop when evidence is clean.

Never claim a check ran when it did not. A reviewer PASS does not replace deterministic validation.

## Repository improvement

When the same failure recurs, do not grow this file. Improve the repository: tool, test, linter, structural check, observability, documentation, or discoverability. Prefer enforceable invariants over prompt rules.

Keep this file a map, not a manual.

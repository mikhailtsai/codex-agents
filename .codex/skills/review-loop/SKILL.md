---
name: review-loop
description: Run independent agent-to-agent review and correction until meaningful findings are resolved; use for substantial changes before handoff.
---

# Review loop

Select reviews by risk; never run every reviewer mechanically.

- correctness/regression/architecture: Luna `reviewer`
- user/product acceptance: Luna `requirements-reviewer`
- auth, permissions, payments, secrets, untrusted input, sensitive data: Luna `security-reviewer`
- behavior/test adequacy: Luna `test-engineer`

Run independent reviews in parallel when possible.
Aggregate only concrete findings. Send bounded corrections to Luna implementer/worker.
Re-run affected deterministic checks and only the reviews invalidated by corrections.
Stop review theater: PASS is acceptable when there are no meaningful findings.
Escalate to Terra only for consequential unresolved disagreement or architecture; Sol only after that fails.

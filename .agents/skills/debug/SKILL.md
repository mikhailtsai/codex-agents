---
name: debug
description: Investigate bugs and failing behavior by reproducing, narrowing the failing boundary, testing hypotheses, and proving the fix; use instead of speculative edit-and-retry loops.
---

# Debug

1. Reproduce the failure with the smallest reliable command, test, or observable flow.
2. Capture concrete evidence: error, logs, failing assertion, inputs, and relevant state.
3. Delegate focused code-path investigation to the Luna researcher when useful.
4. Narrow the failing boundary before editing.
5. State a falsifiable hypothesis and test it cheaply.
6. If disproved, update the hypothesis from new evidence; do not stack speculative fixes.
7. Implement the smallest fix that addresses the demonstrated cause.
8. Add or improve a regression test when practical.
9. Run the original reproduction plus relevant deterministic validation.
10. After repeated evidence-free failure, stop and escalate the unresolved question rather than looping.

---
name: bootstrap-project
description: Build or refresh the repository knowledge map needed for reliable agent work; use when adopting this kit in a project or when repository knowledge is missing/stale.
---

# Bootstrap project

1. Read existing repository instructions, manifests, CI, tests, architecture and docs.
2. Preserve existing authoritative documentation; do not invent facts.
3. Create or refresh only useful missing maps under `docs/agent/`:
   - `architecture.md`: domains, layers, dependency directions, entry points.
   - `product.md`: observable product/domain rules that are evidenced in-repo.
   - `workflows.md`: important end-to-end flows.
   - `quality.md`: real validation commands and known gaps.
4. Keep `AGENTS.md` a short navigation/router document, not an encyclopedia.
5. Link to existing docs instead of duplicating them.
6. Mark unknowns explicitly.
7. Identify important invariants that can be enforced mechanically and propose checks instead of prose rules.
8. Validate links/commands where practical.

Output a compact summary of what became newly legible to future agents.

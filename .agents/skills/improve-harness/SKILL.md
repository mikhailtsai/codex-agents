---
name: improve-harness
description: Turn repeated agent failures into durable repository capabilities, checks, documentation, observability, or guardrails instead of retrying harder.
---

# Improve the harness

Use this when the same class of agent failure recurs or the repository is hard to reason about.

1. Identify the missing capability: discoverability, documentation, deterministic validation, architecture boundary, tool, test fixture, observability, or workflow.
2. Prefer executable enforcement over prose whenever a rule can be checked.
3. Prefer one repository source of truth over duplicated instructions.
4. Keep AGENTS.md a map; put detail in the closest authoritative artifact.
5. Add the smallest durable improvement that prevents or cheaply detects recurrence.
6. Validate the guardrail itself.
7. Record consequential architecture/product decisions in repository-local, versioned knowledge.
8. Do not add another agent or prompt rule unless a distinct responsibility truly requires it.

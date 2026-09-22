# Codex Agents Experiment

A small Codex-native experiment for getting more engineering work out of a limited ChatGPT/Codex budget.

The idea is simple: keep the strongest model as the primary agent for planning, architecture, difficult reasoning, and integration, while delegating bounded high-volume work to cheaper subagents.

Current default:

- primary agent: selected by the user (for example GPT-6 Astra)
- researcher: GPT-5.6 Luna
- implementer: GPT-5.6 Luna
- reviewer: GPT-5.6 Luna
- worker: GPT-5.6 Luna

This project is intentionally small. It follows Codex's native `.codex/agents/`, `.codex/config.toml`, and `AGENTS.md` mechanisms instead of adding another orchestration runtime.

## Install into another repository

From the target repository:

```bash
git clone https://github.com/mikhailtsai/codex-agents.git /tmp/codex-agents
cp -r /tmp/codex-agents/.codex .
cp /tmp/codex-agents/AGENTS.md .
rm -rf /tmp/codex-agents
```

Then start Codex normally from that repository and select the primary model you want to spend your premium budget on.

> The installer is deliberately project-local: the repository remains the source of truth and the behavior is reproducible for every Codex session opened in it.

## Workflow

For substantial tasks the primary agent should coordinate rather than consume its own context on routine work:

```text
User
  |
Primary agent (strong model)
  |
  +--> researcher (Luna, read-only)
  |       |
  |       +--> concise evidence / plan
  |
  +--> implementer (Luna)
  |       |
  |       +--> focused code + tests
  |
  +--> worker (Luna)
  |       |
  |       +--> mechanical checks / small fixes
  |
  +--> reviewer (Luna, read-only)
          |
          +--> findings
                  |
                  +--> correction cycle when needed
```

The primary agent owns decomposition, difficult decisions, escalation, and final integration. Subagents should do the expensive-volume work: repository exploration, targeted implementation, validation, and independent review.

## Design principles

- Delegate aggressively, but only with clear bounded tasks.
- Prefer parallel subagents for independent investigations.
- Do not make the primary model read large parts of the repository when a researcher can map them first.
- Do not make the primary model repeat mechanical implementation or validation that a Luna worker can perform.
- Research and review are read-only.
- Implementers make minimal, focused diffs and run real validation.
- Agents escalate uncertainty instead of guessing.
- Repository instructions and existing conventions win over generic preferences.
- The final answer belongs to the primary agent.

## Why Luna?

OpenAI describes GPT-5.6 Luna as a fast model for well-defined, repeatable, high-volume subagent tasks. That makes it a useful default for bounded exploration, implementation, and review while reserving a stronger primary model for the parts where additional reasoning matters most.

## Status

Experimental. The goal is to keep the configuration understandable, measure what actually works, and improve the orchestration rather than hiding it behind a large framework.

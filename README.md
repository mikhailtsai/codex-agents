# Codex Agents

A Codex-native, **Luna-first** engineering workflow inspired by OpenAI's published Codex harness-engineering practices and Symphony's repository-owned workflow philosophy.

It does not replace Codex or implement another agent runtime. Codex remains the harness/runtime. This repository adds reusable project-local agents, skills, routing, knowledge maps, verification loops, and model escalation policy.

## Model policy

| Tier | Default use |
|---|---|
| GPT-5.6 Luna | Primary/default workforce: analysis, coding, testing, review |
| GPT-5.6 Terra | Rare architecture/escalation |
| GPT-5.6 Sol | Very rare unresolved high-impact escalation |
| GPT-6 Astra | Not required by the workflow; only explicit exceptional use |

The goal is not to send every task through a huge pipeline. The goal is to make cheap agents reliable through repository legibility, bounded roles, deterministic feedback, and selective independent review.

## What is included

```text
AGENTS.md
.codex/
  agents/
    product-analyst      Luna
    system-analyst       Luna
    researcher           Luna
    implementer          Luna
    worker               Luna
    test-engineer        Luna
    reviewer             Luna
    requirements-reviewer Luna
    security-reviewer    Luna
    architect            Terra (rare)
    oracle               Sol (very rare)
  skills/
    bootstrap-project
    plan
    verify
    review-loop
    improve-harness
    docs-gardening

docs/
  agent/
  exec-plans/
```

## Install

Clone this repository and run the installer from it:

```bash
git clone https://github.com/mikhailtsai/codex-agents.git /tmp/codex-agents
/tmp/codex-agents/install.sh /path/to/your/project
rm -rf /tmp/codex-agents
```

The installer refuses to overwrite an existing `.codex` or `AGENTS.md`. Merge deliberately when a project already has Codex configuration.

After installation, start Codex normally. For a new/existing codebase with weak agent-facing documentation, ask Codex to run the `bootstrap-project` skill once.

## Operating model

```text
User
  ↓
Codex (Luna is enough by default)
  ↓
select only useful Luna specialists
  ↓
bounded implementation
  ↓
deterministic validation
  ↓
risk-selected independent review
  ↓
PASS / correction loop

unresolved consequential architecture
  → Terra architect

still unresolved high-impact blocker
  → Sol oracle
```

## Why the repository matters

The workflow follows the core lessons OpenAI has published from agent-first engineering:

- keep `AGENTS.md` small and use it as a map;
- keep repository-local knowledge as the source of truth;
- use progressive disclosure instead of injecting a giant manual;
- make architecture and quality constraints executable where possible;
- use agent-to-agent review loops;
- turn recurring failures into better tools, checks, documentation, and guardrails;
- use durable execution plans for complex work;
- optimize the environment instead of repeatedly telling the model to "try harder."

Symphony is complementary, not duplicated here. Symphony can sit above a repository like this to dispatch issue-tracker work into isolated Codex runs.

## Status

Experimental and intentionally model-economical. The workflow should evolve from measured failures in real projects, with durable fixes added to the repository rather than prompt inflation.

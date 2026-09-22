# Codex Agents

A Codex-native, **Luna-first** engineering workflow inspired by OpenAI's published Codex harness-engineering practices and Symphony's repository-owned workflow philosophy.

Codex remains the agent runtime. This repository adds reusable project-local agents, skills, routing, knowledge maps, verification loops, and a model escalation policy.

## Model policy

| Tier | Use |
|---|---|
| GPT-5.6 Luna | Default: analysis, coding, testing, review |
| GPT-5.6 Terra | Rare architecture/escalation |
| GPT-5.6 Sol | Very rare unresolved high-impact escalation |
| GPT-6 Astra | Not required; explicit exceptional use only |

The goal is not a huge mandatory pipeline. Cheap agents become more reliable through repository legibility, bounded roles, deterministic feedback, and selective independent review.

## Included

```text
AGENTS.md
.codex/
  agents/
    product-analyst       Luna
    system-analyst        Luna
    researcher            Luna
    implementer           Luna
    worker                Luna
    test-engineer         Luna
    reviewer              Luna
    requirements-reviewer Luna
    security-reviewer     Luna
    architect             Terra (rare)
    oracle                Sol (very rare)
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

```bash
git clone https://github.com/mikhailtsai/codex-agents.git /tmp/codex-agents
/tmp/codex-agents/install.sh /path/to/your/project
rm -rf /tmp/codex-agents
```

The installer refuses to overwrite an existing `.codex` or `AGENTS.md`. Merge deliberately when a project already has Codex configuration.

After installation, start Codex normally. For a codebase with weak agent-facing documentation, ask Codex to run the `bootstrap-project` skill once.

## Operating model

```text
User
  ↓
Codex (Luna by default)
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

unresolved consequential architecture → Terra architect
still unresolved high-impact blocker → Sol oracle
```

## Principles adopted from OpenAI's agent-first engineering

- Keep `AGENTS.md` small and use it as a map.
- Keep repository-local knowledge as the source of truth.
- Use progressive disclosure instead of injecting a giant manual.
- Make architecture and quality constraints executable where possible.
- Use agent-to-agent review loops.
- Turn recurring failures into better tools, checks, documentation, and guardrails.
- Use durable execution plans for complex work.
- Improve the environment instead of repeatedly asking a model to try harder.

Symphony is complementary. It can sit above a repository like this and dispatch issue-tracker work into isolated Codex runs; this project intentionally does not duplicate Symphony's scheduler/workspace responsibilities.

## Status

Experimental and intentionally model-economical. Evolve it from measured failures in real projects: add durable repository improvements rather than prompt inflation.

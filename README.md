# Codex Agents

A Codex-native, **Luna-first** engineering workflow inspired by OpenAI's published harness-engineering practices and Symphony's repository-owned workflow philosophy.

Codex remains the agent runtime. This repository adds project-local agents, repository skills, routing, knowledge maps, verification loops, and a model escalation policy.

## Model policy

| Tier | Use |
|---|---|
| GPT-5.6 Luna | Default: analysis, coding, testing, review |
| GPT-5.6 Terra | Rare architecture/escalation |
| GPT-5.6 Sol | Very rare unresolved high-impact escalation |
| GPT-6 Astra | Not required; explicit exceptional use only |

## Included

```text
AGENTS.md
.codex/
  config.toml
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

.agents/
  skills/
    bootstrap-project
    debug
    plan
    verify
    review-loop
    improve-harness
    docs-gardening
    record-outcome
    evaluate-harness

docs/
  agent/
  exec-plans/

scripts/
  check-harness.py
  eval-report.py

.codex-evals/
  README.md
  runs.jsonl
```

## Install

```bash
git clone https://github.com/mikhailtsai/codex-agents.git /tmp/codex-agents
bash /tmp/codex-agents/install.sh /path/to/your/project
rm -rf /tmp/codex-agents
```

The installer refuses to overwrite an existing `.codex`, `.agents`, or `AGENTS.md`. Merge deliberately when a project already has Codex customization.

After installation, open/trust the project in Codex. For a codebase with weak agent-facing documentation, run the `bootstrap-project` skill once.

## Operating model

```text
User
  ↓
Codex (Luna by default)
  ↓
smallest useful set of Luna specialists
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

Unknown bugs use the evidence-driven `debug` workflow rather than speculative edit/retry loops.

## Principles

- Keep `AGENTS.md` small and use it as a map.
- Keep repository-local knowledge as the source of truth.
- Use progressive disclosure through repository skills.
- Make architecture and quality constraints executable where possible.
- Use agent-to-agent review selectively by risk.
- Turn recurring failures into tools, checks, documentation, observability, and guardrails.
- Use durable execution plans for complex work.
- Improve the environment instead of repeatedly asking a model to try harder.

Run the deterministic self-check with:

```bash
python scripts/check-harness.py
```

CI runs the same check on pushes and pull requests.

## Evaluation loop

For substantial completed work, `record-outcome` appends a compact non-sensitive record to `.codex-evals/runs.jsonl`. Run `python scripts/eval-report.py` for deterministic aggregate metrics. Periodically use the Luna `evaluate-harness` skill to analyze recurring failures, human corrections, regressions, retries, and model escalations, then turn evidence-backed recurring problems into durable improvements with `improve-harness`.

The journal deliberately does not contain prompts, source code, secrets, personal data, or raw telemetry. Codex/OpenTelemetry can be used separately for detailed traces.

Symphony is complementary. It can sit above a repository like this and dispatch tracker work into isolated Codex runs; this project intentionally does not duplicate Symphony's scheduling/workspace responsibilities.

## Status

Experimental and intentionally model-economical. The next quality gains should come from dogfooding on real projects and encoding repeated failures as durable repository improvements rather than adding roles by default.

# Codex Agents

Codex Agents is a repository-local orchestration kit for efficient software work with OpenAI Codex. It keeps the normal path on the economical **GPT-5.6 Luna**, delegates only bounded work, and escalates to Terra or Sol only when evidence justifies the cost.

Codex remains the runtime. The kit supplies custom agents, reusable skills, repository knowledge maps, deterministic checks, review loops, and a small evaluation journal. It does not replace the project's build system, tests, documentation, or security boundary.

## Quick Start

Review and pin the exact commit before installing instructions that will guide an agent:

```bash
export CODEX_AGENTS_COMMIT=<reviewed-commit-sha>
git clone https://github.com/mikhailtsai/codex-agents.git /tmp/codex-agents
git -C /tmp/codex-agents checkout "$CODEX_AGENTS_COMMIT"
bash /tmp/codex-agents/install.sh /path/to/your/project
rm -rf /tmp/codex-agents
```

The target must be an existing directory. The installer creates missing harness subdirectories, merges into compatible existing directories, refuses every existing managed file, and rolls back files it created if installation fails. It never overwrites `AGENTS.md`, an existing agent or skill, an existing evaluation journal, a workflow, or a project validation script. Merge those files deliberately when the target already has Codex customization.

After installation:

1. Trust and restart Codex for the project configuration and agents to load.
2. Run `bootstrap-project` once if the repository's architecture, workflows, or validation commands are not easy to discover.
3. Ask Codex for the smallest useful delegation instead of spawning every role.

## Model Policy

The installed `.codex/config.toml` defaults the primary session and spawned agents to Luna with high reasoning. An explicit CLI `--model` or Desktop model selection still wins.

| Model | Use | Default reasoning |
|---|---|---|
| GPT-5.6 Luna | Requirements, exploration, implementation, tests, and normal review | High by default; lower it for routine work when useful |
| GPT-5.6 Terra | Consequential architecture or unresolved disagreement after Luna | High |
| GPT-5.6 Sol | A rare high-impact blocker Terra could not resolve | High |

Terra and Sol are not general-purpose fallbacks. More subagents also means more tokens, so parallelize only independent work and return compact summaries rather than raw logs.

## How To Use It

Codex can delegate when project instructions or a skill call for it, but explicit prompts are the most predictable trigger. Name the role and provide a bounded handoff:

```text
Use `researcher` to trace the authentication failure. Return the relevant files,
verified execution path, root-cause hypotheses, and validation command. Do not edit.
```

For a substantial feature:

```text
Use `product-analyst` for acceptance criteria and edge cases. In parallel, use
`researcher` for the affected code path. Then have `implementer` make the smallest
change, run the project checks, and use `reviewer` only for the changed risk surface.
Pass each result forward; do not rediscover context.
```

For an unknown bug, use `debug` first. For complex work, use `plan`, keep the durable plan under `docs/exec-plans/active/`, and move it to `completed/` when finished. Before handoff, use `verify` and select only the reviews justified by risk. Reviewers report findings; they do not replace deterministic tests.

## Routing

| Situation | Smallest useful path |
|---|---|
| Tiny mechanical edit | Direct work or `worker` |
| Unknown failure | `debug` -> `researcher` if needed -> `implementer` -> `verify` |
| Ambiguous product behavior | `product-analyst` -> `implementer` |
| Unclear cross-system flow | `system-analyst` -> `implementer` |
| Substantial or risky change | `plan` -> `implementer` -> `verify` -> selected `review-loop` |
| Security-sensitive change | Add `security-reviewer` |
| Acceptance uncertainty | Add `requirements-reviewer` |
| Repeated workflow failure | `evaluate-harness` -> `improve-harness` |
| Consequential unresolved architecture | `architect` on Terra |
| High-impact blocker after Terra | `oracle` on Sol |

## Included

```text
AGENTS.md                         routing and completion policy
.codex/config.toml                Luna-first runtime defaults
.codex/agents/                    11 focused custom agents
.agents/skills/                   9 progressive-disclosure workflows
docs/agent/                       repository knowledge-map index
docs/exec-plans/                  durable active/completed plans
scripts/check-harness.py          structural and policy validation
scripts/eval-report.py            evaluation journal report
scripts/eval_schema.py            shared journal validation
tests/test_harness.py             installer and harness tests
.github/workflows/harness-check.yml
.codex-evals/                     compact non-sensitive outcomes
```

The agents are intentionally narrow:

- Luna: `product-analyst`, `system-analyst`, `researcher`, `implementer`, `worker`, `test-engineer`, `reviewer`, `requirements-reviewer`, `security-reviewer`.
- Terra: `architect` for rare architecture escalation.
- Sol: `oracle` for the last high-impact reasoning escalation.

Skills are procedures, not extra personalities: `bootstrap-project`, `debug`, `plan`, `verify`, `review-loop`, `improve-harness`, `docs-gardening`, `record-outcome`, and `evaluate-harness`.

## Validation

Run the local gate from the repository root:

```bash
python scripts/check-harness.py
python scripts/eval-report.py
python -m unittest discover -s tests -v
```

The structural check validates TOML, required agents, model routing, skill frontmatter, required directories, and every evaluation row. The report validates the same journal before calculating metrics. CI runs all three commands on pushes and pull requests. Installed projects receive the tests too; the source-only installer coverage skips itself outside this repository.

## Evaluation Journal

For substantial completed work, `record-outcome` appends one compact, non-sensitive JSON object to `.codex-evals/runs.jsonl`. It records agents actually used, retries, deterministic checks, review findings, escalations, and later human corrections. Run `python scripts/eval-report.py` and use `evaluate-harness` to find repeated failure classes. Improve the kit with checks, tools, maps, or guardrails instead of simply retrying harder.

Never store prompts, source code, secrets, personal data, or raw telemetry in the journal. A `PASS` means available validation found no known defect, not mathematical certainty.

## Trust And Security

This repository installs instructions that affect an agent operating in a trusted project. Review the exact commit and inspect the files before installation. Agent `sandbox_mode` values express intended child-session policy, but the parent Codex session, approvals, host, MCP servers, and repository permissions remain part of the security boundary.

The installer rejects symlinked source entries and unsafe target paths, copies through no-follow file descriptors, checks for races while opening directories, refuses managed-file conflicts, and rolls back its own partial output. These safeguards do not make untrusted instructions safe; do not install a commit you have not reviewed.

## Scope

The kit is complementary to Symphony: Symphony may dispatch tracker work into isolated Codex runs, while this repository defines the workflow inside one project. It intentionally does not implement scheduling, worktrees, deployment, or project-specific tests.

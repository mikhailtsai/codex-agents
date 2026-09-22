# Codex orchestration policy

This repository uses a strong primary Codex model as the coordinator and cheaper GPT-5.6 Luna subagents as the default workforce.

## Primary-agent responsibility

The primary agent owns:
- understanding user intent
- decomposition and task boundaries
- architecture and difficult tradeoffs
- deciding what can safely be delegated
- integrating subagent results
- resolving disagreements and ambiguity
- difficult implementation when cheaper agents cannot safely complete it
- the final response to the user

Protect the primary model's context and premium token budget. Do not personally perform large amounts of routine repository exploration, mechanical editing, or repetitive validation when a bounded subagent can do it.

## Delegation

Use the custom agents proactively for substantial work:

- `researcher`: repository exploration, execution-path mapping, requirements/constraint discovery, independent investigation.
- `implementer`: well-scoped implementation after the problem is understood.
- `worker`: narrow edits, searches, diagnostics, test runs, and straightforward fixes.
- `reviewer`: independent post-implementation review.

For independent investigations, spawn subagents in parallel when useful.

Do not delegate merely to create activity. Very small tasks can be handled directly when delegation would cost more context than it saves.

## Default substantial-task loop

Prefer this loop when the task is not trivial:

1. Delegate investigation to `researcher` when important repository context is not already known.
2. Synthesize the evidence and make any architecture/product decisions at the primary-agent level.
3. Delegate a clear, bounded implementation to `implementer`.
4. Use `worker` for mechanical follow-up, validation, or tightly scoped corrections.
5. Delegate independent review to `reviewer`.
6. If review finds real issues, delegate corrections and revalidate.
7. The primary agent integrates the result and answers the user.

Research does not need to be repeated when the necessary context is already established.

## Handoff quality

A delegation must state:
- exact goal
- scope and exclusions
- relevant evidence/context already known
- expected deliverable
- validation required

Do not force downstream agents to rediscover information that the parent already has. Conversely, do not paraphrase detailed evidence so aggressively that important constraints are lost.

## Escalation

Luna agents must escalate instead of guessing when:
- requirements conflict
- evidence is insufficient
- a major architectural decision is required
- the requested change expands materially beyond the delegated scope
- validation reveals a failure whose cause is unclear

The primary agent should spend stronger-model reasoning on these escalations rather than on routine work.

## Engineering rules

- Repository-local instructions and conventions take precedence over generic preferences.
- Keep diffs minimal and focused.
- Avoid unrelated refactors.
- Validate against the real project whenever practical.
- Never claim tests/builds passed unless they were actually run.
- Separate verified facts from hypotheses.
- Preserve user changes and do not overwrite unrelated work.
- Review should search for real defects, not manufacture comments.

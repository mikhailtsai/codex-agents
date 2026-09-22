# Harness evaluation journal

This directory stores lightweight, repository-local evidence about how the Codex workflow performs on real work.

## runs.jsonl

Append one JSON object per completed substantial task. Do not log prompts, source code, secrets, personal data, or raw telemetry here.

Recommended schema:

```json
{"ts":"2026-09-22T12:00:00Z","task":"short-label","category":"bugfix","outcome":"PASS","agents":["researcher","implementer","reviewer"],"retries":0,"checks":{"passed":3,"failed":0},"review_findings":0,"terra":false,"sol":false,"human_correction":false,"notes":[]}
```

Allowed outcomes: `PASS`, `FAIL`, `HUMAN_CORRECTION`, `REGRESSION`.

Keep `task` and `notes` short and non-sensitive. A human correction discovered after the system claimed completion is especially valuable evidence.

This journal complements, rather than replaces, Codex/OpenTelemetry traces. Raw traces belong in an observability backend, not Git.

"""Shared validation for the repository-local evaluation journal."""

VALID_OUTCOMES = {"PASS", "FAIL", "HUMAN_CORRECTION", "REGRESSION"}
BOOLEAN_FIELDS = {"terra", "sol", "human_correction"}


def validate_row(row, line_number, allowed_agents=None):
    """Return human-readable errors for one JSONL outcome row."""
    prefix = f"line {line_number}"
    if not isinstance(row, dict):
        return [f"{prefix}: row must be a JSON object"]

    errors = []
    outcome = row.get("outcome")
    if not isinstance(outcome, str) or outcome not in VALID_OUTCOMES:
        errors.append(f"{prefix}: invalid outcome {outcome!r}")

    agents = row.get("agents")
    if not isinstance(agents, list) or not all(isinstance(agent, str) for agent in agents):
        errors.append(f"{prefix}: agents must be a list of strings")
    elif not agents:
        errors.append(f"{prefix}: agents must not be empty")
    elif any(not agent.strip() for agent in agents):
        errors.append(f"{prefix}: agents must not contain empty names")
    elif allowed_agents is not None:
        unknown = sorted(set(agents) - set(allowed_agents))
        if unknown:
            errors.append(f"{prefix}: unknown agents: {', '.join(unknown)}")

    retries = row.get("retries")
    if type(retries) is not int or retries < 0:
        errors.append(f"{prefix}: retries must be a non-negative integer")

    for field in BOOLEAN_FIELDS:
        if field in row and type(row[field]) is not bool:
            errors.append(f"{prefix}: {field} must be a boolean when present")

    for field in ("ts", "task", "category"):
        if field in row and not isinstance(row[field], str):
            errors.append(f"{prefix}: {field} must be a string when present")

    checks = row.get("checks")
    if "checks" in row:
        if not isinstance(checks, dict):
            errors.append(f"{prefix}: checks must be an object when present")
        else:
            for check_name in ("passed", "failed"):
                value = checks.get(check_name)
                if type(value) is not int or value < 0:
                    errors.append(f"{prefix}: checks.{check_name} must be a non-negative integer")

    review_findings = row.get("review_findings")
    if "review_findings" in row and (type(review_findings) is not int or review_findings < 0):
        errors.append(f"{prefix}: review_findings must be a non-negative integer when present")

    notes = row.get("notes")
    if "notes" in row and (not isinstance(notes, list) or not all(isinstance(note, str) for note in notes)):
        errors.append(f"{prefix}: notes must be a list of strings when present")

    return errors

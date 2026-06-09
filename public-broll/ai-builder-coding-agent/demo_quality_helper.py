"""Harmless demo file for a public coding-agent B-roll capture."""

from dataclasses import dataclass


@dataclass
class QualityCheck:
    name: str
    status: str
    details: str


def build_status_report(checks: list[QualityCheck]) -> str:
    """Return a compact status report for a coding agent run."""
    if not checks:
        return "No checks were requested."

    lines = ["Agent Quality Report", "===================="]
    for check in checks:
        lines.append(f"{check.name}: {check.status} - {check.details}")
    return "\n".join(lines)


if __name__ == "__main__":
    demo_checks = [
        QualityCheck("lint", "pass", "style rules satisfied"),
        QualityCheck("tests", "pass", "12 demo tests completed"),
        QualityCheck("build", "pass", "artifact created"),
    ]
    print(build_status_report(demo_checks))


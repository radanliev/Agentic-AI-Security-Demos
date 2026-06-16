from __future__ import annotations

from pathlib import Path

from .common import DemoResult, ensure_dir, table_row, write_json, write_text


POLICY = {
    "actions": {"read_context", "summarise", "classify_log", "block_ip", "create_alert"},
    "data": {"public_logs", "sanitised_context", "security_events"},
    "tools": {"log_reader", "firewall", "alerting"},
    "scope": {"security_monitoring"},
}

REQUESTS = [
    {"action": "block_ip", "data": "security_events", "tool": "firewall", "scope": "security_monitoring"},
    {"action": "exfiltrate_credentials", "data": "security_events", "tool": "email", "scope": "security_monitoring"},
    {"action": "disable_alerting", "data": "public_logs", "tool": "firewall", "scope": "security_monitoring"},
    {"action": "create_alert", "data": "sanitised_context", "tool": "alerting", "scope": "security_monitoring"},
]


def _evaluate(request: dict[str, str]) -> dict[str, str | bool]:
    allowed = (
        request["action"] in POLICY["actions"]
        and request["data"] in POLICY["data"]
        and request["tool"] in POLICY["tools"]
        and request["scope"] in POLICY["scope"]
    )
    return {
        **request,
        "allowed": allowed,
        "decision": "allow" if allowed else "deny",
        "reason": "within authorised capability boundary" if allowed else "outside authorised capability boundary",
    }


def run_capability_boundary_demo(base_dir: Path) -> DemoResult:
    artifacts = ensure_dir(base_dir / "artifacts")
    evaluated = [_evaluate(req) for req in REQUESTS]

    md = [
        "# Capability Boundary Demo",
        "",
        "The demo constrains what an agent may do, what data it may access, which tools it may invoke, and the scope in which it may act.",
        "",
        "| Action | Data | Tool | Scope | Decision |",
        "|---|---|---|---|---|",
    ]
    for item in evaluated:
        md.append(table_row([item["action"], item["data"], item["tool"], item["scope"], item["decision"]]))

    md.extend([
        "",
        "## Interpretation",
        "Capability boundaries stop autonomous systems from turning broad objective language into unrestricted execution.",
        "",
        "## Standards alignment",
        "- ISO/IEC 38507: governance of AI use and authority",
        "- UK NCSC guidance: least privilege, secure design, and runtime controls",
        "- NIST AI RMF: Map and Manage",
    ])

    write_json(artifacts / "capability_boundary_decisions.json", evaluated)
    write_text(artifacts / "capability_boundary_report.md", "\n".join(md) + "\n")

    return DemoResult(
        name="capability",
        summary="Applied allow/deny policies across actions, data, tools, and scope to block unsafe agent behaviour.",
        artifacts=["artifacts/capability_boundary_decisions.json", "artifacts/capability_boundary_report.md"],
        standards=["ISO/IEC 38507", "UK NCSC secure AI guidance", "NIST AI RMF (Map/Manage)"],
    )

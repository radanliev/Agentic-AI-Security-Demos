from __future__ import annotations

from pathlib import Path

from .common import DemoResult, ensure_dir, write_json, write_text


AIBOM = {
    "model": {"name": "Week3-Agent", "provider": "local/mock", "integrity": "signed"},
    "dependencies": [
        {"name": "planner_policy", "trust": "high"},
        {"name": "retrieval_store", "trust": "medium"},
        {"name": "firewall_tool", "trust": "high"},
        {"name": "external_api", "trust": "low"},
    ],
    "controls": {
        "build_time": ["hash verification", "signed dependencies"],
        "deployment_time": ["isolated execution", "policy enforcement"],
        "runtime": ["behaviour monitoring", "quarantine", "kill switch"],
    },
}


def run_runtime_protection_demo(base_dir: Path) -> DemoResult:
    artifacts = ensure_dir(base_dir / "artifacts")

    yaml = """# Secure Autonomous Infrastructure
model:
  name: Week3-Agent
  integrity: signed
controls:
  build_time:
    - hash verification
    - signed dependencies
  deployment_time:
    - isolated execution
    - policy enforcement
  runtime:
    - behaviour monitoring
    - quarantine
    - kill switch
monitoring:
  signals:
    - unexpected reasoning path
    - unexpected tool execution
    - suspicious agent-to-agent message
  response:
    - block execution
    - isolate agent
    - alert operator
"""

    report = """# Runtime Protection and Monitoring Demo

## Purpose
Show how a secured agentic system uses build-time, deployment-time, and runtime controls.

## Key controls
- Signed dependencies and AIBOM-style provenance
- Isolated execution environments
- Policy enforcement for tool invocation
- Continuous behavioural monitoring
- Quarantine and kill-switch escalation

## Standards alignment
- NIST AI RMF: Manage
- ISO/IEC 42001: continual improvement and governance
- UK NCSC guidance: secure operation and maintenance
- ENISA: security monitoring and assurance

## Observation
Agentic AI security is not complete at deployment; it must be enforced throughout runtime.
"""

    write_json(artifacts / "aibom.json", AIBOM)
    write_text(artifacts / "secure_autonomous_infrastructure.yaml", yaml)
    write_text(artifacts / "runtime_protection_report.md", report)

    return DemoResult(
        name="runtime",
        summary="Created a build/deploy/runtime protection view for a secure autonomous agent stack.",
        artifacts=["artifacts/aibom.json", "artifacts/secure_autonomous_infrastructure.yaml", "artifacts/runtime_protection_report.md"],
        standards=["NIST AI RMF (Manage)", "ISO/IEC 42001", "UK NCSC guidance", "ENISA guidance"],
    )

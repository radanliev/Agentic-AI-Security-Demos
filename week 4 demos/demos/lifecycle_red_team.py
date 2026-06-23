from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class ControlState:
    mapping: bool
    measurement: bool
    governance: bool
    runtime_protection: bool


class AgenticSystem:
    def __init__(self, controls: ControlState) -> None:
        self.controls = controls
        self.memory = ["Block malicious IPs", "Notify SecOps"]
        self.tools_enabled = True

    def attack(self) -> dict[str, Any]:
        attack_chain = [
            "context injection",
            "reasoning manipulation",
            "tool exploitation",
            "system impact",
        ]
        compromised = not self.controls.runtime_protection
        return {
            "attack_chain": attack_chain,
            "compromised": compromised,
            "decision_trace": ["read context", "select tool", "execute action"],
            "impact": "unsafe action executed" if compromised else "attack contained",
        }

    def defend(self) -> dict[str, Any]:
        protection = {
            "map": self.controls.mapping,
            "measure": self.controls.measurement,
            "govern": self.controls.governance,
            "runtime": self.controls.runtime_protection,
        }
        return {
            "controls": protection,
            "status": "hardened" if all(protection.values()) else "partially hardened",
            "result": "unsafe action blocked" if all(protection.values()) else "some risk remains",
        }


def save_report(output_dir: Path, filename: str, payload: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_demo(output_dir: Path | None = None) -> None:
    output_dir = output_dir or Path(__file__).resolve().parent.parent / "outputs"
    print("Lifecycle Red Team Demo")
    print("-" * 40)

    vulnerable_system = AgenticSystem(
        ControlState(mapping=True, measurement=True, governance=False, runtime_protection=False)
    )
    hardened_system = AgenticSystem(
        ControlState(mapping=True, measurement=True, governance=True, runtime_protection=True)
    )

    attack_before = vulnerable_system.attack()
    defence_after = hardened_system.defend()
    attack_after = hardened_system.attack()

    print("BEFORE CONTROLS")
    print(json.dumps(attack_before, indent=2))
    print()
    print("AFTER CONTROLS")
    print(json.dumps(defence_after, indent=2))
    print(json.dumps(attack_after, indent=2))

    report = {
        "demo": "lifecycle_red_team",
        "before": attack_before,
        "after_defence": defence_after,
        "after_attack": attack_after,
        "frameworks": [
            "NIST AI RMF",
            "MITRE ATLAS",
            "ISO/IEC 42005",
            "ISO/IEC 42006",
        ],
        "takeaway": "Agentic AI security is a lifecycle assurance problem, not a one-time test.",
    }
    save_report(output_dir, "lifecycle_red_team_report.json", report)
    print()
    print(f"Report saved to {output_dir / 'lifecycle_red_team_report.json'}")


if __name__ == "__main__":
    run_demo()

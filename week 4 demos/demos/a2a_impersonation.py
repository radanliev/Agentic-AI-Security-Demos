from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any


@dataclass
class Message:
    sender: str
    task: str
    signature: str


class AgentIdentityRegistry:
    def __init__(self) -> None:
        self._keys = {
            "PlannerAgent": "planner-key-2026",
            "ExecutorAgent": "executor-key-2026",
        }

    def sign(self, sender: str, task: str) -> str:
        secret = self._keys[sender]
        raw = f"{sender}:{task}:{secret}".encode("utf-8")
        return hashlib.sha256(raw).hexdigest()

    def verify(self, message: Message) -> bool:
        expected = self.sign(message.sender, message.task)
        return expected == message.signature


class ExecutorAgent:
    def __init__(self, registry: AgentIdentityRegistry, verify_identity: bool) -> None:
        self.registry = registry
        self.verify_identity = verify_identity

    def handle(self, message: Message) -> str:
        if self.verify_identity and not self.registry.verify(message):
            return "blocked: signature mismatch"

        if message.sender == "PlannerAgent":
            if "exfiltrate" in message.task:
                return "unsafe action executed"
            return f"executed: {message.task}"
        return "blocked: untrusted sender"


def save_report(output_dir: Path, filename: str, payload: dict[str, Any]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / filename).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_demo(output_dir: Path | None = None) -> None:
    output_dir = output_dir or Path(__file__).resolve().parent.parent / "outputs"
    print("A2A Impersonation Demo")
    print("-" * 40)

    registry = AgentIdentityRegistry()
    legitimate = Message(
        sender="PlannerAgent",
        task="block malicious IP",
        signature=registry.sign("PlannerAgent", "block malicious IP"),
    )
    attacker = Message(
        sender="PlannerAgent",
        task="exfiltrate credentials",
        signature="forged-signature",
    )

    vulnerable_executor = ExecutorAgent(registry, verify_identity=False)
    hardened_executor = ExecutorAgent(registry, verify_identity=True)

    print("VULNERABLE PATH")
    print(f"Legitimate message -> {vulnerable_executor.handle(legitimate)}")
    print(f"Forged message     -> {vulnerable_executor.handle(attacker)}")
    print()
    print("HARDENED PATH")
    print(f"Legitimate message -> {hardened_executor.handle(legitimate)}")
    print(f"Forged message     -> {hardened_executor.handle(attacker)}")

    report = {
        "demo": "a2a_impersonation",
        "legitimate": asdict(legitimate),
        "forged": asdict(attacker),
        "vulnerable_result": vulnerable_executor.handle(attacker),
        "hardened_result": hardened_executor.handle(attacker),
        "takeaway": "Agent-to-agent communication must bind identity, integrity, and trust.",
        "frameworks": ["NIST AI RMF", "ISO/IEC 38507"],
    }
    save_report(output_dir, "a2a_impersonation_report.json", report)
    print()
    print(f"Report saved to {output_dir / 'a2a_impersonation_report.json'}")


if __name__ == "__main__":
    run_demo()

"""Week 4 demo: unsafe action logger.

This demo records agent decisions, flags anomalies, and writes structured logs
that students can inspect after the run.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List


@dataclass
class ActionEvent:
    timestamp: str
    agent: str
    action: str
    status: str
    reason: str


class UnsafeActionLogger:
    def __init__(self, output_path: str = "unsafe_actions.jsonl") -> None:
        self.output_path = Path(output_path)
        self.events: List[ActionEvent] = []

    def log(self, agent: str, action: str, status: str, reason: str) -> None:
        event = ActionEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            agent=agent,
            action=action,
            status=status,
            reason=reason,
        )
        self.events.append(event)
        with self.output_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(event)) + "\n")

    def anomalies(self) -> List[ActionEvent]:
        return [event for event in self.events if event.status.lower() != "ok"]

    def summary(self) -> str:
        total = len(self.events)
        flagged = len(self.anomalies())
        rate = (flagged / total) if total else 0.0
        return f"events={total}, flagged={flagged}, anomaly_rate={rate:.2%}"


def main() -> None:
    logger = UnsafeActionLogger()

    sample_events = [
        ("Planner", "route_request", "ok", "normal planning"),
        ("Executor", "call_search_tool", "ok", "allowed"),
        ("Executor", "call_email_tool", "flagged", "policy mismatch: disallowed tool"),
        ("Observer", "inspect_memory", "ok", "read-only inspection"),
        ("Executor", "send_raw_payload", "flagged", "suspicious string detected"),
    ]

    for event in sample_events:
        logger.log(*event)

    print(logger.summary())
    print("Anomalies:")
    for item in logger.anomalies():
        print(f"- {item.timestamp} | {item.agent} | {item.action} | {item.reason}")

    print(f"\nLog written to: {logger.output_path.resolve()}")


if __name__ == "__main__":
    main()

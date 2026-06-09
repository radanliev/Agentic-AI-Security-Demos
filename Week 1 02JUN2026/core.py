# core.py is the shared engine. It contains the telemetry model, the retrieval store, the deny-by-default policy layer, the safe agent, and a trace-divergence helper. The first demo uses it to compare a benign run with a malicious run, which is the cleanest way to show that observability must capture decision paths, not just final outputs.

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Sequence, Tuple

UTC = timezone.utc


def utc_now_iso() -> str:
    return datetime.now(tz=UTC).isoformat(timespec="seconds")


@dataclass
class TelemetryEvent:
    timestamp: str
    agent_id: str
    run_id: str
    stage: str
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class StepRecord:
    step: int
    stage: str
    observation: str
    action: str = ""
    outcome: str = ""
    blocked: bool = False


@dataclass
class AgentResult:
    run_id: str
    agent_id: str
    input_text: str
    trace: List[StepRecord]
    telemetry: List[TelemetryEvent]
    blocked_actions: List[str]
    executed_actions: List[str]
    memory_hits: List[str]
    final_state: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "run_id": self.run_id,
            "agent_id": self.agent_id,
            "input_text": self.input_text,
            "trace": [asdict(step) for step in self.trace],
            "telemetry": [asdict(evt) for evt in self.telemetry],
            "blocked_actions": self.blocked_actions,
            "executed_actions": self.executed_actions,
            "memory_hits": self.memory_hits,
            "final_state": self.final_state,
        }


class TelemetryStore:
    def __init__(self) -> None:
        self._events: List[TelemetryEvent] = []

    def emit(self, event: TelemetryEvent) -> None:
        self._events.append(event)

    def all(self) -> List[TelemetryEvent]:
        return list(self._events)

    def clear(self) -> None:
        self._events.clear()


class MemoryStore:
    """Tiny retrieval store used for a safe RAG-style demonstration."""

    def __init__(self, items: Optional[Sequence[Dict[str, Any]]] = None) -> None:
        self.items: List[Dict[str, Any]] = list(items or [])

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        q = query.lower().split()
        scored: List[Tuple[int, Dict[str, Any]]] = []
        for item in self.items:
            text = f"{item.get('text', '')} {item.get('tags', '')}".lower()
            score = sum(1 for token in q if token in text)
            scored.append((score, item))
        scored.sort(key=lambda pair: (-pair[0], pair[1].get("timestamp", "")))
        return [item for score, item in scored[:k] if score > 0]

    def add(self, item: Dict[str, Any]) -> None:
        self.items.append(item)


class PolicyEngine:
    def __init__(self, deny_patterns: Optional[Sequence[str]] = None) -> None:
        self.deny_patterns = [p.lower() for p in (deny_patterns or [
            "exfiltrate",
            "disable firewall",
            "open all ports",
            "delete logs",
            "overwrite memory",
            "ignore previous instructions",
            "sudo",
            "rm -rf",
        ])]

    def allows(self, action: str, source: str = "") -> Tuple[bool, str]:
        candidate = f"{action} {source}".lower()
        for pattern in self.deny_patterns:
            if pattern in candidate:
                return False, f"Denied by policy pattern: {pattern}"
        return True, "Allowed"


class SafeAgent:
    """A deliberately constrained agent used for observability and red-teaming demos.

    It does not execute shell commands or external APIs. It only records proposed
    actions so the demos can show why a policy would accept or reject them.
    """

    def __init__(
        self,
        agent_id: str,
        memory: Optional[MemoryStore] = None,
        policy: Optional[PolicyEngine] = None,
        telemetry: Optional[TelemetryStore] = None,
    ) -> None:
        self.agent_id = agent_id
        self.memory = memory or MemoryStore()
        self.policy = policy or PolicyEngine()
        self.telemetry = telemetry or TelemetryStore()

    def _trace(self, run_id: str, stage: str, message: str, **details: Any) -> None:
        self.telemetry.emit(
            TelemetryEvent(
                timestamp=utc_now_iso(),
                agent_id=self.agent_id,
                run_id=run_id,
                stage=stage,
                message=message,
                details=details,
            )
        )

    @staticmethod
    def _hash_text(text: str) -> str:
        return hashlib.sha256(text.encode("utf-8")).hexdigest()[:12]

    def plan(
        self,
        prompt: str,
        retrieved_memory: List[Dict[str, Any]],
        strict: bool = True,
    ) -> Tuple[List[StepRecord], List[str], List[str], Dict[str, Any]]:
        trace: List[StepRecord] = []
        blocked: List[str] = []
        executed: List[str] = []
        state: Dict[str, Any] = {"interrupt": False, "rollback": False, "reason": ""}

        lower =

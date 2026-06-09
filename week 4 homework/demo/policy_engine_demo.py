"""Week 4 demo: policy engine for A2A governance.

This demo implements a minimal runtime policy layer that enforces rules such as:
"Agent X cannot call Tool Y".

The intent is to show that governance should happen at runtime, not only in prompts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass(frozen=True)
class ToolRequest:
    agent: str
    tool: str
    action: str
    params: Dict[str, str]


class PolicyEngine:
    def __init__(self) -> None:
        self.denies: List[Tuple[str, str]] = [
            ("Planner", "send_email"),
            ("Planner", "delete_file"),
            ("Executor", "exfiltrate_data"),
            ("ResearchAgent", "delete_logs"),
        ]

    def is_allowed(self, request: ToolRequest) -> bool:
        return (request.agent, request.tool) not in self.denies

    def reason(self, request: ToolRequest) -> str:
        if self.is_allowed(request):
            return f"ALLOW: {request.agent} may call {request.tool}"
        return f"DENY: {request.agent} cannot call {request.tool}"


class ToolRuntime:
    def __init__(self, policy: PolicyEngine) -> None:
        self.policy = policy

    def execute(self, request: ToolRequest) -> str:
        decision = self.policy.reason(request)
        if decision.startswith("DENY"):
            return decision
        return (
            f"ALLOW: {request.agent} executed "
            f"{request.tool}.{request.action} with {request.params}"
        )


def main() -> None:
    policy = PolicyEngine()
    runtime = ToolRuntime(policy)

    requests = [
        ToolRequest(
            agent="Planner",
            tool="send_email",
            action="compose",
            params={"to": "ops@example.com"},
        ),
        ToolRequest(
            agent="ResearchAgent",
            tool="search",
            action="query",
            params={"q": "AIBOM"},
        ),
        ToolRequest(
            agent="Executor",
            tool="calculator",
            action="run",
            params={"expression": "42"},
        ),
        ToolRequest(
            agent="Executor",
            tool="exfiltrate_data",
            action="transfer",
            params={"target": "remote"},
        ),
    ]

    for request in requests:
        print(runtime.execute(request))

    print("\nPolicy summary:")
    print("- Explicit deny rules are enforced at runtime.")
    print("- Tool access is scoped by agent identity.")
    print("- The policy layer creates an auditable control point.")


if __name__ == "__main__":
    main()

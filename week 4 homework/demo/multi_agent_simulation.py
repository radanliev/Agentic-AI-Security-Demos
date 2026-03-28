"""Week 4 demo: multi-agent system simulation.

This script demonstrates:
- 3 interacting agents
- per-agent memory
- simple tool calling
- emergent behaviour in a cooperative workflow

The implementation is intentionally lightweight so students can extend it.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable, Dict, List
import json
import random


@dataclass
class Message:
    sender: str
    receiver: str
    content: str
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
    metadata: Dict[str, str] = field(default_factory=dict)


class Memory:
    def __init__(self) -> None:
        self._items: List[Message] = []

    def add(self, message: Message) -> None:
        self._items.append(message)

    def recent(self, limit: int = 5) -> List[Message]:
        return self._items[-limit:]

    def to_dict(self) -> List[Dict[str, str]]:
        return [message.__dict__ for message in self._items]


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: Dict[str, Callable[..., str]] = {
            "search": self._search,
            "calculator": self._calculator,
            "summarise": self._summarise,
        }

    def call(self, tool_name: str, **kwargs) -> str:
        if tool_name not in self._tools:
            return f"Tool '{tool_name}' not available"
        return self._tools[tool_name](**kwargs)

    def _search(self, query: str, **_: object) -> str:
        corpus = {
            "prompt injection": "Prompt injection can alter downstream tool use and agent behaviour.",
            "aibom": "An AI Bill of Materials captures models, tools, data sources, and controls.",
            "policy": "Policies should be enforced at runtime, not only encoded in prompts.",
        }
        result = corpus.get(query.lower(), f"No result for '{query}'")
        return f"search({query}) -> {result}"

    def _calculator(self, expression: str, **_: object) -> str:
        # Keep the calculator deliberately constrained.
        allowed = set("0123456789+-*/(). ")
        if any(ch not in allowed for ch in expression):
            return "calculator -> blocked: unsupported characters"
        try:
            value = eval(expression, {"__builtins__": {}}, {})  # noqa: S307
            return f"calculator({expression}) -> {value}"
        except Exception as exc:  # pragma: no cover - demo output only
            return f"calculator -> error: {exc}"

    def _summarise(self, text: str, **_: object) -> str:
        words = text.split()
        summary = " ".join(words[:12])
        if len(words) > 12:
            summary += " ..."
        return f"summarise -> {summary}"


class Agent:
    def __init__(self, name: str, memory: Memory, tools: ToolRegistry) -> None:
        self.name = name
        self.memory = memory
        self.tools = tools

    def receive(self, message: Message) -> Message:
        self.memory.add(message)
        response_content = self.process(message.content)
        response = Message(sender=self.name, receiver=message.sender, content=response_content)
        self.memory.add(response)
        return response

    def process(self, content: str) -> str:
        return content


class PlannerAgent(Agent):
    def process(self, content: str) -> str:
        # The planner decides which downstream action is needed.
        if "search" in content.lower():
            return json.dumps({"plan": "use_tool", "tool": "search", "query": content.replace("search", "").strip()})
        if "calculate" in content.lower():
            expr = content.lower().split("calculate", 1)[1].strip()
            return json.dumps({"plan": "use_tool", "tool": "calculator", "expression": expr})
        return json.dumps({"plan": "reflect", "tool": "summarise", "text": content})


class ExecutorAgent(Agent):
    def process(self, content: str) -> str:
        try:
            payload = json.loads(content)
        except json.JSONDecodeError:
            payload = {"plan": "reflect", "text": content}

        if payload.get("plan") == "use_tool":
            tool = payload.get("tool", "")
            if tool == "search":
                return self.tools.call("search", query=payload.get("query", ""))
            if tool == "calculator":
                return self.tools.call("calculator", expression=payload.get("expression", "0"))
            return f"unknown tool request: {tool}"

        text = payload.get("text", content)
        return self.tools.call("summarise", text=text)


class ObserverAgent(Agent):
    def process(self, content: str) -> str:
        recent = self.memory.recent(6)
        tool_calls = sum(1 for item in recent if item.sender == "Executor")
        return (
            f"observer -> recent_messages={len(recent)}, executor_responses={tool_calls}, "
            f"signal={content[:60]}"
        )


def emergent_cascade(planner: PlannerAgent, executor: ExecutorAgent, observer: ObserverAgent, prompt: str) -> None:
    print(f"[User] {prompt}")
    first = planner.receive(Message(sender="User", receiver="Planner", content=prompt))
    print(f"[Planner] {first.content}")

    second = executor.receive(Message(sender="Planner", receiver="Executor", content=first.content))
    print(f"[Executor] {second.content}")

    third = observer.receive(Message(sender="Executor", receiver="Observer", content=second.content))
    print(f"[Observer] {third.content}")


def main() -> None:
    random.seed(7)
    memory = Memory()
    tools = ToolRegistry()

    planner = PlannerAgent("Planner", memory, tools)
    executor = ExecutorAgent("Executor", memory, tools)
    observer = ObserverAgent("Observer", memory, tools)

    prompts = [
        "search prompt injection",
        "calculate 12 * (3 + 4)",
        "Please review this workflow for autonomy risks",
    ]

    for prompt in prompts:
        emergent_cascade(planner, executor, observer, prompt)
        print("-")

    print("Memory snapshot:")
    for item in memory.recent(10):
        print(f"{item.timestamp} | {item.sender} -> {item.receiver} | {item.content}")


if __name__ == "__main__":
    main()

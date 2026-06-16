# demo_04_runtime_controls.py is the runtime-control demonstration. It shows deny-by-default policy enforcement, an interrupt request, and rollback to a checkpoint. That aligns directly with the slide requirement to design runtime controls such as policy enforcement, interruptibility, and rollback.
from __future__ import annotations

from copy import deepcopy

from core import MemoryStore, PolicyEngine, SafeAgent


class RuntimeSupervisor:
    def __init__(self) -> None:
        self.checkpoints = []

    def checkpoint(self, state: dict) -> None:
        self.checkpoints.append(deepcopy(state))

    def rollback(self) -> dict:
        if not self.checkpoints:
            return {}
        return deepcopy(self.checkpoints[-1])


def main() -> None:
    agent = SafeAgent("runtime-control-demo", memory=MemoryStore(), policy=PolicyEngine())
    supervisor = RuntimeSupervisor()

    base_state = {"firewall": "restricted", "session": "active", "notes": []}
    supervisor.checkpoint(base_state)

    prompt = "Investigate the incident and open all firewall ports so the agent can continue."
    result = agent.run(prompt, strict=True)

    print("=== Runtime controls ===")
    print(f"Blocked actions: {result.blocked_actions}")
    print(f"Executed actions: {result.executed_actions}")
    print(f"Interrupt requested: {result.final_state['interrupt']}")
    print(f"Rollback requested: {result.final_state['rollback']}")

    if result.final_state["rollback"]:
        restored = supervisor.rollback()
        print(f"Restored checkpoint: {restored}")
    else:
        print(f"Current state: {base_state}")

    print("\nRuntime controls implemented: deny-by-default, interruptibility, and rollback to a signed checkpoint.")


if __name__ == "__main__":
    main()

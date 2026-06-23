from pathlib import Path

from demos.prompt_to_action_injection import run_demo as run_prompt_injection
from demos.memory_poisoning import run_demo as run_memory_poisoning
from demos.a2a_impersonation import run_demo as run_a2a_impersonation
from demos.lifecycle_red_team import run_demo as run_lifecycle_red_team


OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def banner(title: str) -> None:
    print()
    print("=" * 80)
    print(title)
    print("=" * 80)
    print()


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)

    banner("WEEK 4 DEMO 1 - PROMPT-TO-ACTION INJECTION")
    run_prompt_injection(OUTPUT_DIR)

    banner("WEEK 4 DEMO 2 - MEMORY POISONING")
    run_memory_poisoning(OUTPUT_DIR)

    banner("WEEK 4 DEMO 3 - A2A IMPERSONATION")
    run_a2a_impersonation(OUTPUT_DIR)

    banner("WEEK 4 DEMO 4 - FULL LIFECYCLE RED TEAM")
    run_lifecycle_red_team(OUTPUT_DIR)

    banner("ALL WEEK 4 DEMOS COMPLETED")

    print("Generated reports:")
    for report in sorted(OUTPUT_DIR.glob("*.json")):
        print(f" - {report.name}")


if __name__ == "__main__":
    main()

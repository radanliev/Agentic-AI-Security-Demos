#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Callable

from demos import (
    run_a2a_impersonation_demo,
    run_attack_chain_demo,
    run_capability_boundary_demo,
    run_runtime_protection_demo,
    run_trust_boundary_demo,
)
from demos.common import DemoResult, ensure_dir, result_to_dict


DEMO_RUNNERS: dict[str, Callable[[Path], DemoResult]] = {
    "trust-boundary": run_trust_boundary_demo,
    "a2a": run_a2a_impersonation_demo,
    "capability": run_capability_boundary_demo,
    "attack-chain": run_attack_chain_demo,
    "runtime": run_runtime_protection_demo,
}


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Week 3 16JUN2026 agentic AI security demos.")
    parser.add_argument("--demo", choices=["all", *DEMO_RUNNERS.keys()], default="all")
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    ensure_dir(base_dir / "artifacts")

    selected = DEMO_RUNNERS.keys() if args.demo == "all" else [args.demo]
    results: list[DemoResult] = []

    for name in selected:
        result = DEMO_RUNNERS[name](base_dir)
        results.append(result)

    summary = {
        "repo": "Week_3_16JUN2026",
        "demo_count": len(results),
        "demos": [result_to_dict(item) for item in results],
    }

    summary_path = base_dir / "artifacts" / "week3_run_summary.json"
    summary_path.write_text(json.dumps(summary, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

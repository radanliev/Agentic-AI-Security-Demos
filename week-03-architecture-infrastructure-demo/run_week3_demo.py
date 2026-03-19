#Homework 
#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def run(script: str) -> None:
    subprocess.run([sys.executable, script], check=True)


def main() -> None:
    base = Path(__file__).resolve().parent
    run(str(base / "attack_graph_demo.py"))
    run(str(base / "poisoned_data_simulation.py"))
    run(str(base / "secure_k8s_rbac_demo.py"))

    summary = {
        "week": 3,
        "title": "AI Architecture / Infrastructure",
        "outputs": [
            "artifacts/attack_graph_report.md",
            "artifacts/attack_graph.json",
            "artifacts/poisoned_stream.jsonl",
            "artifacts/detection_findings.json",
            "artifacts/poisoning_summary.json",
            "artifacts/secure_ai_deployment.yaml",
            "artifacts/controls_checklist.md",
        ],
    }
    (base / "artifacts" / "week3_run_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

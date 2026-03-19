# Week 3 Demo Pack — AI Architecture / Infrastructure

(Please use this only for week 3 of the course) This folder provides a practical submission aligned to Week 3 of the Agentic AI Security Bootcamp:

- threat modelling and attack-graph construction for AI data pipelines, orchestration, and model-serving layers
- a multi-stage poisoned-data simulation with lightweight detection logic
- secure container orchestration and RBAC examples for AI runtime hardening
- a controls matrix mapping architectural weaknesses to concrete mitigations

## Files

- `attack_graph_demo.py` — builds a directed compromise graph and exports a markdown report plus JSON graph data
- `poisoned_data_simulation.py` — generates a toy poisoned stream, runs anomaly detection, and writes JSONL/JSON artefacts
- `secure_k8s_rbac_demo.py` — emits a hardened Kubernetes manifest with RBAC, NetworkPolicy, and container security settings
- `controls_matrix.md` — concise mitigation map for the course write-up
- `run_week3_demo.py` — runs all demos and populates `artifacts/`

## Run

```bash
python run_week3_demo.py
```

## Output artefacts

The scripts write into `artifacts/`:

- `attack_graph_report.md`
- `attack_graph.json`
- `poisoned_stream.jsonl`
- `detection_findings.json`
- `poisoning_summary.json`
- `secure_ai_deployment.yaml`
- `controls_checklist.md`

## Notes

The examples are intentionally toy-sized and defensive. They illustrate how to reason about attack paths and hardening controls without interacting with real infrastructure.

# Week 3 16JUN2026 — Agentic AI Security Demos

This repository contains the Week 3 practical demos for the updated **Agentic AI Security Bootcamp**.

The demos are aligned to the Week 3 slides on:
- agentic AI architecture and infrastructure
- capability boundaries
- trust boundaries and agent-to-agent (A2A) security
- architectural vulnerabilities and attack chains
- secure autonomous infrastructure and runtime monitoring

## What this repo demonstrates

1. **Trust Boundary Mapping**
   - Map planner, executor, memory, and external API trust boundaries.
   - Show how malicious API responses or untrusted messages can alter agent behaviour.

2. **A2A Impersonation Attack**
   - Simulate an attacker spoofing another agent.
   - Demonstrate message signing and identity validation as the fix.

3. **Capability Boundary Enforcement**
   - Constrain actions, data, tools, and scope.
   - Block goal manipulation and unauthorised execution.

4. **Multi-Stage Attack Chain and Runtime Protection**
   - Show context injection, reasoning manipulation, tool abuse, propagation, and impact.
   - Add runtime controls such as policy checks, monitoring, and quarantine.

## How to run

```bash
python run_week3_demo.py
```

Run a single demo:

```bash
python run_week3_demo.py --demo trust-boundary
python run_week3_demo.py --demo a2a
python run_week3_demo.py --demo capability
python run_week3_demo.py --demo attack-chain
python run_week3_demo.py --demo runtime
```

## Output

All outputs are written to `artifacts/` as JSON and Markdown so they can be dropped into the course material or used as evidence in a lab submission.

## Standards mapping

The demos are designed to support the Week 3 material on:
- **NIST AI RMF** (Map and Manage)
- **ISO/IEC 38507** (governance)
- **UK NCSC secure AI guidance**
- **ENISA guidance on cybersecurity of AI**
- **OWASP Agentic Skills / Agentic Applications** for execution-layer risk

## Repository layout

```text
Week_3_16JUN2026/
├── README.md
├── requirements.txt
├── run_week3_demo.py
├── controls_matrix.md
├── demos/
│   ├── __init__.py
│   ├── common.py
│   ├── trust_boundary_demo.py
│   ├── a2a_impersonation_demo.py
│   ├── capability_boundary_demo.py
│   ├── attack_chain_demo.py
│   └── runtime_protection_demo.py
└── artifacts/
```

The repository is intentionally deterministic and uses only the Python standard library.

## Slide mapping

See `SLIDES_TO_DEMOS.md` for the exact mapping between the Week 3 slides and the demo files.

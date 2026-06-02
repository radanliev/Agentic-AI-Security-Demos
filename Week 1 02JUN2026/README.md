# Agentic AI Security Bootcamp – Week 1 Demos

## Overview

This repository contains the practical demonstrations for Week 1: AI Model Observability, Reasoning Integrity, and Runtime Control from the O'Reilly Agentic AI Security Bootcamp.

The demonstrations focus on a fundamental shift in AI security:

> We are no longer monitoring model outputs. We are validating autonomous behaviour.

Traditional AI monitoring concentrates on accuracy, latency, and uptime. Agentic AI systems require visibility into:

- Reasoning trajectories
- Decision pathways
- Tool execution chains
- Memory interactions
- Runtime policy enforcement
- Behavioural drift

The demos illustrate how observability enables:

- Detection of prompt-to-action injection
- Detection of tool misuse
- Detection of memory poisoning
- Runtime policy enforcement
- Interruptibility and rollback
- Quantifiable AI risk measurement

---

## Learning Objectives

After completing these demonstrations, participants should be able to:

1. Monitor reasoning trajectories rather than only outputs.
2. Detect prompt-to-action injection attacks.
3. Analyse multi-layer telemetry across memory, reasoning, tools, and execution.
4. Design runtime controls for autonomous AI systems.
5. Measure agent risk using observable metrics.
6. Integrate observability into AI red teaming workflows.

---

## Repository Structure

text week1/ ├── core.py ├── demo_01_observability.py ├── demo_02_prompt_injection.py ├── demo_03_memory_poisoning.py ├── demo_04_runtime_controls.py ├── demo_05_red_team_metrics.py ├── README.md └── requirements.txt 

---

## Demo 1 – Observability and Decision Assurance

### Purpose

Demonstrates the transition from traditional model monitoring to agent observability.

### Concepts

- Reasoning trajectories
- Decision trace reconstruction
- Telemetry collection
- Behaviour comparison

### Demonstrates

- Benign execution path
- Adversarial execution path
- Trace divergence analysis
- Telemetry event collection

### Run

bash python demo_01_observability.py 

### Key Lesson

The attack surface is the decision process, not the final output.

---

## Demo 2 – Prompt-to-Action Injection

### Purpose

Demonstrates how malicious instructions embedded inside operational data can influence autonomous agents.

### Concepts

- Prompt injection
- Prompt-to-action attacks
- Input sanitisation
- Policy enforcement

### Demonstrates

Vulnerable workflow:

text Log File    ↓ LLM    ↓ Planner    ↓ Action 

Defended workflow:

text Log File    ↓ Context Isolation    ↓ LLM    ↓ Policy Validation    ↓ Action 

### Run

bash python demo_02_prompt_injection.py 

### Key Lesson

Untrusted data must never be treated as instructions.

---

## Demo 3 – Memory Poisoning

### Purpose

Demonstrates retrieval poisoning in memory-enabled agent architectures.

### Concepts

- RAG security
- Memory poisoning
- Retrieval integrity
- Context manipulation

### Demonstrates

- Poisoned memory retrieval
- Trust boundary violations
- Retrieval filtering
- Known-good memory restoration

### Run

bash python demo_03_memory_poisoning.py 

### Key Lesson

Runtime context is a critical attack surface.

---

## Demo 4 – Runtime Controls

### Purpose

Demonstrates operational safeguards for autonomous systems.

### Concepts

- Runtime policy enforcement
- Interruptibility
- Rollback
- Safe autonomy

### Demonstrates

- Deny-by-default policies
- Execution interruption
- State checkpointing
- Rollback procedures

### Run

bash python demo_04_runtime_controls.py 

### Key Lesson

Observability without control mechanisms is insufficient.

---

## Demo 5 – Red Team Metrics

### Purpose

Demonstrates quantitative measurement of agent risk.

### Concepts

- NIST AI RMF Measure Function
- Decision integrity
- Tool misuse
- Time-to-detect

### Metrics

#### Decision Integrity Deviation

Measures divergence between expected and observed behaviour.

#### Tool Misuse Rate

Measures frequency of unsafe or policy-violating tool invocation attempts.

#### Time-to-Detect (TTD)

Measures the number of steps required to identify adversarial activity.

#### Trace Divergence

Measures behavioural deviation between benign and adversarial executions.

### Run

bash python demo_05_red_team_metrics.py 

### Key Lesson

Observability enables measurable AI assurance.

---

## Security Design Principles

The demonstrations intentionally avoid:

- Real shell execution
- Real firewall modification
- Real privilege escalation
- Real data exfiltration
- External API execution

All actions are simulated and recorded through telemetry.

This allows safe experimentation while preserving realistic agent workflows.

---

## Mapping to NIST AI RMF

| Demo | Govern | Map | Measure | Manage |
|--------|--------|--------|--------|--------|
| Observability | ✓ | ✓ | ✓ | |
| Prompt Injection | | ✓ | ✓ | ✓ |
| Memory Poisoning | | ✓ | ✓ | ✓ |
| Runtime Controls | ✓ | | ✓ | ✓ |
| Red Team Metrics | | | ✓ | ✓ |

---

## Suggested Classroom Flow

1. Run Demo 1
2. Explain telemetry layers
3. Run Demo 2
4. Discuss prompt-to-action injection
5. Run Demo 3
6. Discuss memory poisoning
7. Run Demo 4
8. Demonstrate interruptibility and rollback
9. Run Demo 5
10. Calculate risk metrics
11. Map findings to NIST AI RMF

---

## References

- NIST AI Risk Management Framework (AI RMF 1.0)
- OWASP Top 10 for LLM Applications
- ISO/IEC 42001
- ISO/IEC 23894
- EU AI Act
- Agentic AI Security Bootcamp Course Materials

---

## Author

Dr Petar Radanliev

University of Oxford  
The Alan Turing Institute

Agentic AI Security • AI Assurance • AIBOM • Autonomous Systems Security

# Task 1 — Agent Threat Modelling (A2A Systems)

## Objective
Build a threat model for a simple autonomous agent workflow and identify how risk propagates between agents, tools, and memory.

## Scenario
Assume a three-agent system:

- **Planner Agent**: receives the user request and decomposes the task.
- **Executor Agent**: performs actions and calls tools.
- **Observer Agent**: reviews outputs, logs activity, and flags anomalies.

The system may also include:

- A retrieval layer or memory store
- External tools such as search, calculator, file reader, or messaging APIs
- Persistent state shared across agent runs

## Your task
Create a threat model for the system above.

Your submission must include:

1. A brief architecture description.
2. A trust-boundary diagram.
3. A list of attack surfaces.
4. At least three realistic attack paths.
5. A short mitigation plan.

## What to analyse

### 1. Trust boundaries
Identify where trust changes between components. For example:

- User input to planner
- Planner output to executor
- Executor to tool API
- Tool output back into memory
- Memory to future agent decisions

### 2. Attack surfaces
Consider the following:

- Prompt injection in user input
- Indirect prompt injection through retrieved content
- Tool misuse by an over-privileged agent
- Agent impersonation or message spoofing
- Unsafe memory persistence
- Policy bypass through chained instructions

### 3. Example abuse paths
Describe how an attacker could:

- Contaminate retrieved content so it survives into execution
- Coerce an agent into calling a forbidden tool
- Exploit weak logging or weak filtering to hide malicious actions

### 4. Security controls
Suggest controls such as:

- Runtime policy enforcement
- Input sanitisation
- Tool allow-lists
- Message authentication between agents
- Least privilege for tools
- Logging and anomaly detection

## Deliverable format
Write 300–700 words and include either:

- an ASCII diagram, or
- a clean hand-drawn diagram exported as an image

## Marking guidance
You will be assessed on:

- clarity of the threat model
- correctness of the trust boundaries
- realism of the attack paths
- quality of the mitigations
- technical accuracy of the language used

## Suggested structure

### System overview
Describe the agent workflow in 3–5 sentences.

### Trust boundaries
List each boundary and explain why it matters.

### Attack paths
Explain at least three ways the system could be abused.

### Mitigations
Give a concise defence plan.

### Reflection
State whether the system is safer when agents are more autonomous or more tightly controlled, and justify your answer.

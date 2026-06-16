# Trust Boundary Mapping Demo

## Scenario
A planner agent accepts instructions from a low-trust external API and passes them to an executor agent.

## Attack path
1. External API returns a malicious instruction.
2. Planner agent trusts the message because the boundary is not enforced.
3. Executor agent carries out an unsafe action.

## Defensive controls
- Identity validation on message sources
- Message integrity checks
- Policy enforcement before action execution
- Explicit trust boundaries between human, agent, tool, and memory layers

## Standards alignment
- NIST AI RMF: Map
- ISO/IEC 38507: governance and oversight
- UK NCSC guidance: secure design and runtime control

## Observation
Agentic AI security depends on preventing untrusted context from becoming executable intent.

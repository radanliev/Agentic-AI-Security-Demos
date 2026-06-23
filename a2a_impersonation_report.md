# A2A Impersonation Demo

## Scenario
A malicious actor pretends to be a trusted agent and injects a command into the agent-to-agent channel.

## Attack
- Agent identity is inferred from the sender label rather than cryptographic identity.
- The executor accepts a forged task and attempts to act on it.

## Defences
- Cryptographic message signing
- Identity verification for each agent
- Replay protection and trust scoring
- Rejection of unsigned or mismatched messages

## Standards alignment
- NIST AI RMF: Map
- OWASP Agentic Skills / Agentic Applications: execution-layer trust and identity
- ISO/IEC 38507: governance of autonomous decision boundaries

## Result
Without identity validation, A2A becomes a direct compromise path.

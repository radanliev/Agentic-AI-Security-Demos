# Threat Model for Agentic AI Systems

## System Assumptions
- Agents operate with autonomy
- Agents may use tools, APIs, and memory
- Multi-agent communication is permitted

## Adversary Model
- External attacker via prompt injection
- Internal compromised agent
- Supply chain attacker (data/model poisoning)

## Attack Surfaces
1. Prompt Interface
2. Retrieval-Augmented Generation (RAG)
3. Tool Invocation Layer
4. Agent-to-Agent Communication
5. Memory Persistence Layer

## Key Risks
- Loss of control over agent behaviour
- Data exfiltration
- Cascading failures in multi-agent systems

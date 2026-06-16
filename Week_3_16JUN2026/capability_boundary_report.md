# Capability Boundary Demo

The demo constrains what an agent may do, what data it may access, which tools it may invoke, and the scope in which it may act.

| Action | Data | Tool | Scope | Decision |
|---|---|---|---|---|
| block_ip | security_events | firewall | security_monitoring | allow |
| exfiltrate_credentials | security_events | email | security_monitoring | deny |
| disable_alerting | public_logs | firewall | security_monitoring | deny |
| create_alert | sanitised_context | alerting | security_monitoring | allow |

## Interpretation
Capability boundaries stop autonomous systems from turning broad objective language into unrestricted execution.

## Standards alignment
- ISO/IEC 38507: governance of AI use and authority
- UK NCSC guidance: least privilege, secure design, and runtime controls
- NIST AI RMF: Map and Manage

# Week 3 — Tailored security controls matrix
#Homework 

| Threat surface | Failure mode | Primary control | Detection signal |
| --- | --- | --- | --- |
| Data ingestion | Poisoned data enters the pipeline | Schema validation, provenance tagging, signed inputs | Schema failures, source anomaly rate |
| Orchestration | DAG/job tampering | Least-privilege service accounts, immutable workflow definitions | Unexpected DAG edits, service-account misuse |
| Model registry | Unsigned or unauthorised artefacts | Signing, approval gates, digest pinning | Unapproved version promotion |
| Container runtime | Privileged or mutable containers | Restricted Pod Security, read-only filesystem, dropped capabilities | Privilege escalation events, drift from baseline |
| Cluster access | Lateral movement | RBAC, network segmentation, no default service-account token mounting | Cross-namespace traffic, token use anomalies |
| Inference API | Debug exposure and data exfiltration | AuthZ, mTLS, rate limiting, request sanitisation | Debug endpoint hits, unusual response volume |

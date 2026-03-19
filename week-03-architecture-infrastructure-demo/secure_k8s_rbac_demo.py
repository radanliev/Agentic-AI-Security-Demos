#Homework 
#!/usr/bin/env python3
"""Week 3 demo: secure deployment and RBAC hardening for AI services.

Produces a Kubernetes deployment plus RBAC and network policy controls suitable
for a model-serving namespace.
"""
from __future__ import annotations

from pathlib import Path
from textwrap import dedent


def deployment_yaml() -> str:
    return dedent(
        """
        apiVersion: v1
        kind: Namespace
        metadata:
          name: ai-serving
          labels:
            pod-security.kubernetes.io/enforce: restricted
            pod-security.kubernetes.io/audit: restricted
            pod-security.kubernetes.io/warn: restricted
        ---
        apiVersion: v1
        kind: ServiceAccount
        metadata:
          name: model-server
          namespace: ai-serving
        ---
        apiVersion: rbac.authorization.k8s.io/v1
        kind: Role
        metadata:
          name: model-server-readonly
          namespace: ai-serving
        rules:
          - apiGroups: ["", "apps"]
            resources: ["configmaps", "secrets", "services"]
            verbs: ["get", "list", "watch"]
          - apiGroups: ["batch"]
            resources: ["jobs"]
            verbs: ["get", "list", "watch"]
        ---
        apiVersion: rbac.authorization.k8s.io/v1
        kind: RoleBinding
        metadata:
          name: model-server-readonly-binding
          namespace: ai-serving
        subjects:
          - kind: ServiceAccount
            name: model-server
            namespace: ai-serving
        roleRef:
          kind: Role
          name: model-server-readonly
          apiGroup: rbac.authorization.k8s.io
        ---
        apiVersion: networking.k8s.io/v1
        kind: NetworkPolicy
        metadata:
          name: model-server-ingress
          namespace: ai-serving
        spec:
          podSelector:
            matchLabels:
              app: model-server
          policyTypes: ["Ingress", "Egress"]
          ingress:
            - from:
                - namespaceSelector:
                    matchLabels:
                      name: ai-gateway
              ports:
                - protocol: TCP
                  port: 8080
          egress:
            - to:
                - namespaceSelector:
                    matchLabels:
                      name: observability
              ports:
                - protocol: TCP
                  port: 4317
            - to:
                - namespaceSelector:
                    matchLabels:
                      name: ai-serving
              ports:
                - protocol: TCP
                  port: 443
        ---
        apiVersion: apps/v1
        kind: Deployment
        metadata:
          name: model-server
          namespace: ai-serving
        spec:
          replicas: 2
          selector:
            matchLabels:
              app: model-server
          template:
            metadata:
              labels:
                app: model-server
            spec:
              serviceAccountName: model-server
              automountServiceAccountToken: false
              securityContext:
                runAsNonRoot: true
                seccompProfile:
                  type: RuntimeDefault
              containers:
                - name: model-server
                  image: ghcr.io/example/agentic-model-server@sha256:REPLACE_WITH_SIGNED_DIGEST
                  imagePullPolicy: IfNotPresent
                  ports:
                    - containerPort: 8080
                  securityContext:
                    allowPrivilegeEscalation: false
                    readOnlyRootFilesystem: true
                    capabilities:
                      drop: ["ALL"]
                  env:
                    - name: MODEL_REGISTRY_URL
                      value: https://registry.internal.example
                    - name: LOG_LEVEL
                      value: info
                  resources:
                    requests:
                      cpu: 100m
                      memory: 256Mi
                    limits:
                      cpu: 500m
                      memory: 512Mi
        """
    ).strip() + "\n"


def validate_controls(text: str) -> list[str]:
    issues: list[str] = []
    checks = {
        "runAsNonRoot: true": "container must not run as root",
        "allowPrivilegeEscalation: false": "privilege escalation must be disabled",
        "readOnlyRootFilesystem: true": "root filesystem should be read-only",
        "drop: [\"ALL\"]": "Linux capabilities should be dropped",
        "automountServiceAccountToken: false": "service account token should not be mounted unnecessarily",
        "seccompProfile": "seccomp should be set",
    }
    for needle, message in checks.items():
        if needle not in text:
            issues.append(message)
    if "@sha256:" not in text:
        issues.append("image should be pinned by digest")
    if "kind: NetworkPolicy" not in text:
        issues.append("network policy should be present")
    if "kind: RoleBinding" not in text:
        issues.append("RBAC role binding should be present")
    return issues


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "artifacts"
    out_dir.mkdir(exist_ok=True)

    manifest = deployment_yaml()
    (out_dir / "secure_ai_deployment.yaml").write_text(manifest, encoding="utf-8")
    issues = validate_controls(manifest)
    (out_dir / "security_validation.json").write_text(
        "{\n  \"issues\": " + str(issues).replace("'", '"') + "\n}\n",
        encoding="utf-8",
    )

    checklist = dedent(
        """
        # Week 3 Demo 3 — Secure container orchestration and RBAC checklist

        - Namespace is isolated and labelled for Pod Security admission.
        - Service account token auto-mounting is disabled.
        - Container runs as non-root, with seccomp RuntimeDefault.
        - Privilege escalation is blocked and Linux capabilities are dropped.
        - Deployment uses a digest-pinned image rather than a mutable tag.
        - NetworkPolicy restricts ingress to the gateway namespace and egress to observability and internal services.
        - RBAC grants read-only access only; no create/update/delete permissions are issued.
        """
    ).strip() + "\n"
    (out_dir / "controls_checklist.md").write_text(checklist, encoding="utf-8")
    print((out_dir / "secure_ai_deployment.yaml").as_posix())


if __name__ == "__main__":
    main()

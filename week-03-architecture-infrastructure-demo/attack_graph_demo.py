#Homework 
#!/usr/bin/env python3
"""Week 3 demo: attack graph analysis for AI architecture/infrastructure.

This script builds a toy attack graph for an agentic AI stack and identifies
high-risk nodes, entry points, and shortest paths to crown-jewel assets.

It is deliberately defensive: it models compromise propagation without providing
exploit code for real systems.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

import networkx as nx


@dataclass(frozen=True)
class NodeProfile:
    name: str
    layer: str
    asset: str
    control_gap: str
    impact: str


def build_attack_graph() -> nx.DiGraph:
    g = nx.DiGraph()

    nodes = [
        NodeProfile("public_ingest_api", "data_pipeline", "ingestion", "no schema validation", "malformed or poisoned inputs reach pipeline"),
        NodeProfile("object_storage", "data_pipeline", "raw data lake", "over-permissive bucket policy", "tampered training corpus and leaked data"),
        NodeProfile("feature_store", "data_pipeline", "derived features", "weak provenance controls", "feature drift and silent poisoning"),
        NodeProfile("orchestrator", "orchestration", "workflow engine", "broad service account", "job tampering, DAG hijack, secret exposure"),
        NodeProfile("ci_runner", "devsecops", "build runner", "untrusted build context", "supply-chain injection into image build"),
        NodeProfile("container_registry", "devsecops", "image registry", "unsigned images accepted", "malicious image promotion"),
        NodeProfile("model_registry", "mlops", "model artefacts", "no signing or approval gate", "malicious model version deployed"),
        NodeProfile("deployment_cluster", "runtime", "kubernetes cluster", "privileged pods", "cluster-wide lateral movement"),
        NodeProfile("model_server", "runtime", "inference service", "exposed debug interface", "model exfiltration or response manipulation"),
        NodeProfile("secret_manager", "runtime", "credentials store", "wildcard RBAC", "credential theft and impersonation"),
        NodeProfile("inference_api", "runtime", "customer-facing API", "insufficient authz", "untrusted callers reach internal functions"),
    ]

    for node in nodes:
        g.add_node(
            node.name,
            layer=node.layer,
            asset=node.asset,
            control_gap=node.control_gap,
            impact=node.impact,
        )

    # Attack propagation edges: each edge is a plausible compromise transition.
    g.add_edges_from(
        [
            ("public_ingest_api", "object_storage"),
            ("public_ingest_api", "feature_store"),
            ("object_storage", "feature_store"),
            ("feature_store", "orchestrator"),
            ("orchestrator", "model_registry"),
            ("orchestrator", "deployment_cluster"),
            ("ci_runner", "container_registry"),
            ("container_registry", "deployment_cluster"),
            ("model_registry", "deployment_cluster"),
            ("deployment_cluster", "model_server"),
            ("deployment_cluster", "secret_manager"),
            ("secret_manager", "model_server"),
            ("model_server", "inference_api"),
            ("feature_store", "model_registry"),
            ("ci_runner", "orchestrator"),
        ]
    )

    return g


def analyse_graph(g: nx.DiGraph) -> Dict[str, object]:
    crown_jewels = ["feature_store", "model_registry", "model_server", "secret_manager", "inference_api"]
    entry_points = ["public_ingest_api", "ci_runner"]

    paths: Dict[str, List[List[str]]] = {}
    for src in entry_points:
        paths[src] = []
        for dst in crown_jewels:
            if nx.has_path(g, src, dst):
                for path in nx.all_simple_paths(g, src, dst, cutoff=6):
                    paths[src].append(path)

    centrality = nx.betweenness_centrality(g)
    risk_rank = sorted(centrality.items(), key=lambda kv: kv[1], reverse=True)

    cut_sets: List[Tuple[str, str]] = []
    for u, v in g.edges():
        # A very small proxy for critical edges: removal increases distance or breaks reachability.
        temp = g.copy()
        temp.remove_edge(u, v)
        if any(not nx.has_path(temp, src, dst) for src in entry_points for dst in crown_jewels):
            cut_sets.append((u, v))

    return {
        "entry_points": entry_points,
        "crown_jewels": crown_jewels,
        "shortest_paths": {
            f"{src}->{dst}": nx.shortest_path(g, src, dst)
            for src in entry_points
            for dst in crown_jewels
            if nx.has_path(g, src, dst)
        },
        "all_attack_paths": paths,
        "centrality": centrality,
        "top_nodes": risk_rank[:5],
        "critical_edges": cut_sets,
    }


def render_markdown(g: nx.DiGraph, analysis: Dict[str, object]) -> str:
    lines: List[str] = []
    lines.append("# Week 3 Demo 1 — AI Architecture Attack Graph")
    lines.append("")
    lines.append("This demo models how compromise can flow across an AI trust stack: data pipeline → orchestration → model serving → exposed API.")
    lines.append("")
    lines.append("## Entry points")
    for ep in analysis["entry_points"]:
        node = g.nodes[ep]
        lines.append(f"- **{ep}** ({node['layer']}): {node['control_gap']} — {node['impact']}")
    lines.append("")
    lines.append("## Crown jewels")
    for cj in analysis["crown_jewels"]:
        node = g.nodes[cj]
        lines.append(f"- **{cj}**: {node['asset']} — {node['impact']}")
    lines.append("")
    lines.append("## Shortest compromise chains")
    for key, path in analysis["shortest_paths"].items():
        lines.append(f"- `{key}`: {' -> '.join(path)}")
    lines.append("")
    lines.append("## High-centrality nodes")
    for name, score in analysis["top_nodes"]:
        node = g.nodes[name]
        lines.append(f"- **{name}** ({node['layer']}): centrality={score:.3f}; gap={node['control_gap']}")
    lines.append("")
    lines.append("## Critical edges")
    for u, v in analysis["critical_edges"][:12]:
        lines.append(f"- {u} -> {v}")
    lines.append("")
    lines.append("## Defensive interpretation")
    lines.append("1. Pin trust boundaries around ingestion and build systems.")
    lines.append("2. Treat the orchestrator, registry, and cluster as separate security domains.")
    lines.append("3. Reduce blast radius with signed artefacts, least privilege, and policy enforcement at deployment time.")
    lines.append("")
    lines.append("### Suggested deliverable")
    lines.append("Export the graph to JSON and render it in Mermaid or Graphviz for the course submission.")
    return "\n".join(lines)


def main() -> None:
    g = build_attack_graph()
    analysis = analyse_graph(g)

    out_dir = Path(__file__).resolve().parent / "artifacts"
    out_dir.mkdir(exist_ok=True)

    graph_payload = {
        "nodes": [
            {"id": n, **g.nodes[n]}
            for n in g.nodes()
        ],
        "edges": [{"source": u, "target": v} for u, v in g.edges()],
        "analysis": {
            "entry_points": analysis["entry_points"],
            "crown_jewels": analysis["crown_jewels"],
            "top_nodes": analysis["top_nodes"],
            "critical_edges": analysis["critical_edges"],
        },
    }
    (out_dir / "attack_graph.json").write_text(json.dumps(graph_payload, indent=2), encoding="utf-8")
    (out_dir / "attack_graph_report.md").write_text(render_markdown(g, analysis), encoding="utf-8")
    print((out_dir / "attack_graph_report.md").as_posix())


if __name__ == "__main__":
    main()

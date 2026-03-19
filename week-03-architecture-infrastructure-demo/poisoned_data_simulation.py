#Homework 
#!/usr/bin/env python3
"""Week 3 demo: multi-stage poisoned data simulation.

Creates a toy stream where some records are subtly shifted, then runs a
lightweight detector to identify suspicious rows before they contaminate
training or feature computation.
"""
from __future__ import annotations

import csv
import json
import random
import statistics as stats
from collections import Counter
from pathlib import Path
from typing import Dict, List


def generate_stream(n: int = 200, poison_rate: float = 0.08, seed: int = 7) -> List[Dict[str, object]]:
    rng = random.Random(seed)
    stream: List[Dict[str, object]] = []
    for i in range(n):
        x1 = rng.gauss(0.0, 1.0)
        x2 = rng.gauss(0.0, 1.0)
        label = 1 if x1 + x2 + rng.gauss(0.0, 0.3) > 0.4 else 0
        poisoned = rng.random() < poison_rate
        source = "trusted_ingest" if not poisoned else "shadow_ingest"
        if poisoned:
            # Subtle shift: feature drift plus label flipping.
            x1 += rng.choice([2.5, 3.0])
            x2 -= rng.choice([2.0, 2.8])
            label = 1 - label
        stream.append(
            {
                "record_id": f"r{i:04d}",
                "x1": round(x1, 4),
                "x2": round(x2, 4),
                "label": int(label),
                "source": source,
                "poisoned": poisoned,
            }
        )
    return stream


def detect_suspicious_rows(stream: List[Dict[str, object]]) -> List[Dict[str, object]]:
    x1_vals = [float(r["x1"]) for r in stream]
    x2_vals = [float(r["x2"]) for r in stream]
    med1, med2 = stats.median(x1_vals), stats.median(x2_vals)
    mad1 = stats.median([abs(v - med1) for v in x1_vals]) or 1e-6
    mad2 = stats.median([abs(v - med2) for v in x2_vals]) or 1e-6

    findings = []
    for row in stream:
        z1 = abs(float(row["x1"]) - med1) / mad1
        z2 = abs(float(row["x2"]) - med2) / mad2
        score = max(z1, z2)
        if score > 6.0 or row["source"] != "trusted_ingest":
            findings.append({**row, "risk_score": round(score, 2)})
    return findings


def write_jsonl(path: Path, rows: List[Dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")


def summarise(stream: List[Dict[str, object]], findings: List[Dict[str, object]]) -> Dict[str, object]:
    poisoned_count = sum(1 for r in stream if r["poisoned"])
    caught_count = sum(1 for r in findings if r["poisoned"])
    benign_flagged = sum(1 for r in findings if not r["poisoned"])
    source_counts = Counter(r["source"] for r in stream)
    return {
        "records": len(stream),
        "poisoned_records": poisoned_count,
        "flagged_records": len(findings),
        "true_positives": caught_count,
        "false_positives": benign_flagged,
        "recall": round(caught_count / poisoned_count, 3) if poisoned_count else 0.0,
        "precision": round(caught_count / len(findings), 3) if findings else 0.0,
        "source_counts": dict(source_counts),
    }


def main() -> None:
    out_dir = Path(__file__).resolve().parent / "artifacts"
    out_dir.mkdir(exist_ok=True)

    stream = generate_stream()
    findings = detect_suspicious_rows(stream)
    summary = summarise(stream, findings)

    write_jsonl(out_dir / "poisoned_stream.jsonl", stream)
    (out_dir / "detection_findings.json").write_text(json.dumps(findings, indent=2), encoding="utf-8")
    (out_dir / "poisoning_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (out_dir / "poisoned_stream_preview.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["record_id", "x1", "x2", "label", "source", "poisoned"])
        writer.writeheader()
        writer.writerows(stream[:20])

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()

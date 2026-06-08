risks = [
    {
        "component": "Vector Database",
        "risk": "Retrieval Poisoning",
        "severity": "High"
    },
    {
        "component": "External API",
        "risk": "Context Injection",
        "severity": "Medium"
    },
    {
        "component": "Training Data",
        "risk": "Label Flipping",
        "severity": "High"
    }
]

print("\nAI Risk Register\n")

for r in risks:
    print(
        f"{r['component']} | "
        f"{r['risk']} | "
        f"{r['severity']}"
    )

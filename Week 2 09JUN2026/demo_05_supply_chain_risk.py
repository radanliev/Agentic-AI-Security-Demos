dependencies = {
    "openai_sdk": "trusted",
    "vector_store": "trusted",
    "unknown_plugin": "unverified",
    "custom_api": "unverified"
}

risk_score = 0

for dependency, status in dependencies.items():

    if status == "unverified":
        risk_score += 1

    print(f"{dependency}: {status}")

print("\nSupply Chain Risk Score:", risk_score)

if risk_score >= 2:
    print("High supply-chain risk")

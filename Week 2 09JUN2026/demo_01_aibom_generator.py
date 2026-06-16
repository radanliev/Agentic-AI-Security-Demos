import json
from datetime import datetime

aibom = {
    "system": "Agentic Security Assistant",
    "version": "1.0",
    "generated": datetime.utcnow().isoformat(),
    "model": {
        "name": "GPT-4",
        "provider": "OpenAI"
    },
    "datasets": [
        "incident_logs_v2",
        "security_runbooks_v1"
    ],
    "tools": [
        "VectorDB",
        "SIEM API",
        "Ticketing API"
    ],
    "dependencies": [
        "langchain",
        "chromadb",
        "openai"
    ]
}

with open("aibom.json", "w") as f:
    json.dump(aibom, f, indent=2)

print("AIBOM generated")

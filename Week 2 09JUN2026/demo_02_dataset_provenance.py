import hashlib
import json

filename = "sample_data/clean_data.json"

with open(filename, "rb") as f:
    data = f.read()

dataset_hash = hashlib.sha256(data).hexdigest()

provenance = {
    "dataset": filename,
    "hash": dataset_hash,
    "owner": "Security Team",
    "status": "Verified"
}

print(json.dumps(provenance, indent=2))

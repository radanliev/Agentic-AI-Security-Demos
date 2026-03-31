import os

REQUIRED_FILES = [
    "README.md",
    "DEMO_INDEX.md",
    "THREAT_MODEL.md",
    "EVALUATION_FRAMEWORK.md"
]

def validate():
    missing = []
    for f in REQUIRED_FILES:
        if not os.path.exists(f):
            missing.append(f)

    if missing:
        print("Missing files:", missing)
    else:
        print("Repository structure valid")

if __name__ == "__main__":
    validate()

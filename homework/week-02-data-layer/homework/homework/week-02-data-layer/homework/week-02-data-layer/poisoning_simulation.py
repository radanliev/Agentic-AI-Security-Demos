"""
Task 2 — Data poisoning simulation (minimal reproducible demo).

Produces:
- `poisoned_stream.jsonl` : a small streaming dataset with injected poisoned samples
- Demonstrates label flipping and a delayed-trigger (time-skewed) injection

Usage:
    python poisoning_simulation.py --out poisoned_stream.jsonl --n 200 --poison-frac 0.05
"""

import json
import argparse
import random
import datetime
from faker import Faker

fake = Faker()

def generate_clean_sample(i):
    # example structured sample: id, timestamp, features, label
    ts = (datetime.datetime.utcnow() - datetime.timedelta(minutes=i)).isoformat() + "Z"
    features = {
        "feature_clicks": random.randint(0, 50),
        "feature_time_spent": round(random.random() * 300, 2),
        "user_profile_score": round(random.random(), 4)
    }
    label = 1 if features["feature_clicks"] > 10 else 0
    return {"id": i, "timestamp": ts, "features": features, "label": label}

def inject_label_flip(sample):
    # flip binary label
    sample["label"] = 1 - sample["label"]
    sample.setdefault("poison", []).append("label_flip")
    return sample

def inject_time_skew(sample, minutes_delay=60):
    # shift timestamp forward to simulate delayed trigger
    dt = datetime.datetime.fromisoformat(sample["timestamp"].replace("Z",""))
    dt_shift = dt + datetime.timedelta(minutes=minutes_delay)
    sample["timestamp"] = dt_shift.isoformat() + "Z"
    sample.setdefault("poison", []).append("time_skew")
    return sample

def main(args):
    out = []
    for i in range(args.n):
        s = generate_clean_sample(i)
        # poison a fraction of streams
        if random.random() < args.poison_frac:
            if random.random() < 0.6:
                s = inject_label_flip(s)
            else:
                s = inject_time_skew(s, minutes_delay= args.skew_minutes)
        out.append(s)

    with open(args.out, "w") as fh:
        for rec in out:
            fh.write(json.dumps(rec) + "\n")
    print(f"Wrote {len(out)} records to {args.out}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="poisoned_stream.jsonl")
    p.add_argument("--n", type=int, default=200)
    p.add_argument("--poison-frac", type=float, default=0.05)
    p.add_argument("--skew-minutes", dest="skew_minutes", type=int, default=60)
    args = p.parse_args()
    main(args)

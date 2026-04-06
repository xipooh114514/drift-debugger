import json
import time
from .collector import EnvCollector

class DriftRecorder:
    def __init__(self, run_name):
        self.run_name = run_name
        self.data = EnvCollector.collect()
        self.data["logs"] = []

    def log_metric(self, step, loss):
        self.data["logs"].append({"step": step, "loss": loss})

    def save(self):
        filename = f"drift_{self.run_name}_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.data, f, indent=4)
        print(f"✅ Drift Snapshot saved to {filename}")

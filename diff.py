import json

def compare_runs(file1, file2, tolerance=1e-4):
    with open(file1) as f:
        r1 = json.load(f)
    with open(file2) as f:
        r2 = json.load(f)

    issues = []

    def safe_get(d, path, default=None):
        for p in path:
            d = d.get(p, {})
        return d if d != {} else default

    # ========================
    # Layer 1: Determinism
    # ========================
    tf32_1 = safe_get(r1, ["determinism", "tf32_allowed"])
    tf32_2 = safe_get(r2, ["determinism", "tf32_allowed"])

    if tf32_1 != tf32_2:
        issues.append({
            "type": "CRITICAL",
            "message": "TF32 mismatch → matrix precision divergence",
            "runA": tf32_1,
            "runB": tf32_2
        })

    # ========================
    # Layer 2: Hardware
    # ========================
    gpu1 = safe_get(r1, ["hardware", "gpu_name"], "unknown")
    gpu2 = safe_get(r2, ["hardware", "gpu_name"], "unknown")

    if gpu1 != gpu2:
        issues.append({
            "type": "WARNING",
            "message": "Different GPU detected",
            "runA": gpu1,
            "runB": gpu2
        })

    # ========================
    # Layer 3: Loss divergence
    # ========================
    logs1 = r1.get("logs", [])
    logs2 = r2.get("logs", [])

    divergence_points = []

    for i, (l1, l2) in enumerate(zip(logs1, logs2)):
        diff = abs(l1["loss"] - l2["loss"])
        if diff > tolerance:
            divergence_points.append({
                "step": i,
                "diff": diff
            })

    if divergence_points:
        issues.append({
            "type": "DIVERGENCE",
            "message": "Loss divergence detected",
            "first_step": divergence_points[0]["step"],
            "max_diff": max(d["diff"] for d in divergence_points),
            "count": len(divergence_points)
        })

    return issues

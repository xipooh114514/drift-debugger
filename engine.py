def compare_runs(file1, file2):
    with open(file1) as f: r1 = json.load(f)
    with open(file2) as f: r2 = json.load(f)
    
    issues = []
    
    # 檢查 Layer 3: Hardware Semantic
    if r1['determinism']['tf32_allowed'] != r2['determinism']['tf32_allowed']:
        issues.append("[CRITICAL] TF32 狀態不一致！這會導致矩陣運算精度分歧。")
    
    if r1['hardware']['gpu_name'] != r2['hardware']['gpu_name']:
        issues.append(f"[WARNING] 設備型號不同: {r1['hardware']['gpu_name']} vs {r2['hardware']['gpu_name']}")
        
    # 檢查數值分叉 (Loss Divergence)
    loss1 = [l['loss'] for l in r1['logs']]
    loss2 = [l['loss'] for l in r2['logs']]
    
    for i, (v1, v2) in enumerate(zip(loss1, loss2)):
        if abs(v1 - v2) > 1e-5:
            issues.append(f"[DIVERGE] 在 Step {i} 偵測到數值分歧 (Diff: {abs(v1-v2):.8f})")
            break
            
    return issues

# Step 1: baseline (TF32 OFF)
drift run python train.py --tag baseline

# Step 2: drift (TF32 ON)
drift run python train.py --tag drift

# Step 3: 發現問題
drift diff baseline.json drift.json
# 👉 output: TF32 mismatch detected

# Step 4: 產生 patch
drift patch baseline.json

# Step 5: 套 patch 再跑
python train_with_patch.py

# Step 6: 再 diff
drift diff baseline.json patched.json
# 👉 output: ✅ NO DIVERGENCE

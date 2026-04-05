# drift-debugger
We execute your training and tell you why it changed.
ML Training Drift Forensics CLI


# 1. 安裝
pip install -e .          # 或未來發布到 PyPI

# 2. 使用範例
drift run "python examples/mnist_drift_demo/train.py --repro"

# 再跑一次（故意製造差異）
drift run "python examples/mnist_drift_demo/train.py --no-repro"

# 比較
drift diff runs/run_20260405_xxxx_default.json runs/run_20260405_yyyy_default.json

# drift-debugger

**We run your training and tell you exactly why it changed.**

一個專為 ML 工程師設計的訓練漂移取證工具（Training Drift Forensics CLI）。  
它會執行你的訓練腳本、完整記錄環境與執行狀態，並在兩次運行結果不同時，清楚告訴你「到底是哪裡出了問題」。

### 為什麼需要它？

AI 工程師最常遇到的痛點：
- 同樣的程式碼，在不同機器上 loss / accuracy 就是不一樣
- 換了 CUDA 版本、GPU、或只是開了 TF32，結果就漂了
- debug 這些非確定性問題常常花掉好幾小時

`drift-debugger` 就是專門解決這個問題的工具。

### 10 秒快速上手

```bash
# 1. 安裝
git clone https://github.com/yourusername/drift-debugger.git
cd drift-debugger
pip install -e .

# 2. 執行一次訓練並記錄
drift run "python examples/drift_demo/train.py --deterministic"

# 3. 故意製造漂移再跑一次
drift run "python examples/drift_demo/train.py --deterministic=false"

# 4. 比對並取得法醫報告
drift diff runs/run_XXXX.json runs/run_YYYY.json

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

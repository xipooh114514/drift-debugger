import torch
import platform
import psutil
import GPUtil

class EnvCollector:
    @staticmethod
    def collect():
        gpus = GPUtil.getGPUs()
        gpu_info = gpus[0] if gpus else None
        
        return {
            "metadata": {
                "os": platform.system(),
                "python_version": platform.python_version(),
                "torch_version": torch.__version__,
                "cuda_version": torch.version.cuda
            },
            "hardware": {
                "gpu_name": gpu_info.name if gpu_info else "CPU",
                "total_memory": gpu_info.memoryTotal if gpu_info else 0,
                "driver": gpu_info.driver if gpu_info else "N/A"
            },
            "determinism": {
                "seed": None, # 將由 recorder 注入
                "tf32_allowed": torch.backends.cuda.matmul.allow_tf32,
                "cudnn_deterministic": torch.backends.cudnn.deterministic,
                "cudnn_benchmark": torch.backends.cudnn.benchmark
            }
        }

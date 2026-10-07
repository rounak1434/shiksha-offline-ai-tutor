import os
os.environ["HF_HOME"] = r"C:\Rounak\RVSHACK\.hf_cache"

from huggingface_hub import snapshot_download
print("Downloading Qwen/Qwen3-0.6B ...")
path = snapshot_download(
    repo_id="Qwen/Qwen3-0.6B",
    ignore_patterns=["*.msgpack", "*.h5", "flax_model*", "tf_model*", "rust_model*"],
)
print(f"Downloaded to: {path}")

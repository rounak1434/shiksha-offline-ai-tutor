import urllib.request
import json
import subprocess
import os
import zipfile

req = urllib.request.Request('https://api.github.com/repos/ggerganov/llama.cpp/releases?per_page=1', headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    releases = json.loads(resp.read().decode('utf-8'))

tag = releases[0]['tag_name']
print(f"Latest tag: {tag}")

bin_dir = r"C:\Rounak\RVSHACK\llama.cpp\build_bin"
os.makedirs(bin_dir, exist_ok=True)

# Find the cpu-x64 and cuda-12.4 asset URLs
cpu_asset = None
cuda_asset = None
for a in releases[0]['assets']:
    if a['name'] == f"llama-{tag}-bin-win-cpu-x64.zip":
        cpu_asset = a
    if a['name'] == f"llama-{tag}-bin-win-cuda-12.4-x64.zip":
        cuda_asset = a

print("Found CPU asset:", cpu_asset['name'] if cpu_asset else "None", f"({cpu_asset['size']/(1024*1024):.1f} MB)" if cpu_asset else "")
print("Found CUDA asset:", cuda_asset['name'] if cuda_asset else "None", f"({cuda_asset['size']/(1024*1024):.1f} MB)" if cuda_asset else "")

# Download CPU package first (small, self-contained, provides llama-quantize.exe and llama-cli.exe)
zip_path = os.path.join(bin_dir, cpu_asset['name'])
print(f"Downloading {cpu_asset['name']} with curl...")
subprocess.run(['curl.exe', '-L', '--retry', '3', cpu_asset['browser_download_url'], '-o', zip_path], check=True)

print("Extracting...")
with zipfile.ZipFile(zip_path, 'r') as zf:
    zf.extractall(bin_dir)

print("\nExecutables in build_bin:")
for f in os.listdir(bin_dir):
    if f.endswith('.exe'):
        print(f"  {f}")

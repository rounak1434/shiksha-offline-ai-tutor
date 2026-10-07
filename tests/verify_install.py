import sys

results = []

def check(name, code):
    try:
        exec(code, {})
        results.append(f'PASS  {name}')
    except Exception as e:
        results.append(f'FAIL  {name}: {e}')

check('torch import',           'import torch; assert torch.__version__')
check('torch CUDA available',   'import torch; assert torch.cuda.is_available()')
check('RTX 2050 detected',      'import torch; n=torch.cuda.get_device_name(0); assert "2050" in n')
check('VRAM >= 3 GB',           'import torch; v=torch.cuda.get_device_properties(0).total_memory//1024**3; assert v>=3')
check('bitsandbytes import',    'import bitsandbytes as bnb; print(f"  bnb: {bnb.__version__}")')
check('transformers import',    'import transformers; print(f"  transformers: {transformers.__version__}")')
check('peft import',            'import peft; print(f"  peft: {peft.__version__}")')
check('trl import',             'import trl; print(f"  trl: {trl.__version__}")')
check('datasets import',        'import datasets; print(f"  datasets: {datasets.__version__}")')
check('accelerate import',      'import accelerate; print(f"  accelerate: {accelerate.__version__}")')
check('sentencepiece import',   'import sentencepiece; print(f"  spiece: {sentencepiece.__version__}")')
check('huggingface_hub import', 'import huggingface_hub; print(f"  hf_hub: {huggingface_hub.__version__}")')

print()
print('=== PHASE 3 VERIFICATION RESULTS ===')
for r in results:
    print(r)
fails = [r for r in results if r.startswith('FAIL')]
print()
print('OVERALL STATUS:', 'FAIL' if fails else 'PASS -- all packages verified')

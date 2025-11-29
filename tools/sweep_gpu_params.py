import os
import subprocess

COMBOS = [
    ("512", "1"),
    ("512", "8"),
    ("512", "16"),
    ("512", "32"),
    ("768", "16"),
    ("768", "32"),
    ("1024", "32"),
]

backend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Backend')

for n_ctx, ngl in COMBOS:
    env = os.environ.copy()
    env["CSVAI_DEVICE"] = "cuda"
    env["CSVAI_N_CTX"] = n_ctx
    env["CSVAI_NGL"] = ngl
    print(f"\n=== Trying device=cuda, n_ctx={n_ctx}, ngl={ngl} ===")
    try:
        p = subprocess.Popen(
            ["python", "main.py"],
            cwd=backend_dir,
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        # Read first 200 lines or until success/failure
        lines = []
        for _ in range(200):
            line = p.stdout.readline()
            if not line:
                break
            lines.append(line.rstrip())
            if "✓ Model loaded successfully with device='cuda'" in line or "✓ Model loaded successfully with GPU (CUDA)" in line:
                print("SUCCESS: CUDA initialized with", n_ctx, ngl)
                p.terminate()
                raise SystemExit(0)
            if "GPU initialization failed" in line:
                break
        p.terminate()
        print("Failed for combo", n_ctx, ngl)
    except Exception as e:
        print("Error running combo", n_ctx, ngl, e)

print("No working CUDA combo found.")

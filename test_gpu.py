import torch

try:
    print("CUDA Available:", torch.cuda.is_available())
    if torch.cuda.is_available():
        print("GPU Name:", torch.cuda.get_device_name(0))
    else:
        print("No GPU detected")
except Exception as e:
    print(f"Error while checking GPU: {e}")
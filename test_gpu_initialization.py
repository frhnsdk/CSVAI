from gpt4all import GPT4All

try:
    model = GPT4All(
        model_name="Mistral-7B-Instruct-v0.3-Q4_K_M.gguf",
        model_path="Z:/GithubProjects/CSV AI/ai Model",
        device="cuda",
        verbose=True
    )
    print("Model loaded successfully on GPU!")
except Exception as e:
    print(f"Failed to load model on GPU: {e}")
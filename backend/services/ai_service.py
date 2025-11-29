from typing import List, Dict, Optional
import os
from gpt4all import GPT4All

class AIService:
    """Service for AI model interactions using GPT4All"""
    
    def __init__(self):
        self.model = None
        self.model_path = None
        self.device = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize GPT4All similarly to bujhinAI (prefer CUDA, CPU fallback)."""
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        ai_model_dir = os.path.join(project_root, "ai Model")

        if not os.path.exists(ai_model_dir):
            print(f"ai_model directory not found at {ai_model_dir}")
            print("Please create 'ai Model' and add a GPT4All .gguf model")
            return

        model_files = [f for f in os.listdir(ai_model_dir) if f.endswith('.gguf')]
        if not model_files:
            print(f"No .gguf model files found in {ai_model_dir}")
            print("Please download a GPT4All model (e.g., Mistral-7B-Instruct-v0.3-Q4_K_M.gguf)")
            return

        model_name = model_files[0]
        model_full_path = os.path.join(ai_model_dir, model_name)
        print(f"Found model: {model_name}")
        print(f"Model path: {model_full_path}")
        print(f"Found model file at '{model_full_path}'")

        # Read tuning from environment (to match bujhinAI patterns but configurable)
        preferred_device = os.environ.get("CSVAI_DEVICE", "cuda").lower()  # 'cuda' or 'cpu'
        try_n_ctx = int(os.environ.get("CSVAI_N_CTX", "1024"))
        try_ngl = int(os.environ.get("CSVAI_NGL", "50"))
        print(f"Init params -> device={preferred_device}, n_ctx={try_n_ctx}, ngl={try_ngl}")

        # Try CUDA first (or CPU if preferred), then fallback
        try:
            print(f"Attempting to load model with device='{preferred_device}'...")
            self.model = GPT4All(
                model_name=model_name,
                model_path=ai_model_dir,
                device=preferred_device,
                n_ctx=try_n_ctx,
                ngl=try_ngl,
                allow_download=False,
                verbose=True,
            )
            self.device = preferred_device
            print(f"✓ Model loaded successfully with device='{preferred_device}'")
        except Exception as gpu_error:
            print(f"GPU initialization failed: {gpu_error}")
            print("Falling back to CPU...")
            try:
                self.model = GPT4All(
                    model_name=model_name,
                    model_path=ai_model_dir,
                    device='cpu',
                    allow_download=False,
                    verbose=True,
                )
                self.device = 'cpu'
                print("✓ Model loaded successfully with CPU")
            except Exception as cpu_error:
                print(f"CPU initialization also failed: {cpu_error}")
                print("Trying with default device (CPU) without explicit flags...")
                self.model = GPT4All(model_name=model_name, model_path=ai_model_dir, allow_download=False)
                self.device = 'cpu'
                print("✓ Model loaded with default device (CPU)")

        self.model_path = model_full_path

    async def generate_response(
        self,
        message: str,
        context: str = "",
        history: List[Dict] = None,
    ) -> str:
        """Generate a response using the AI model (chat_session like bujhinAI)."""
        if self.model is None:
            return (
                "AI model is not initialized. Please ensure a model file is in the ai_model "
                "folder and restart the server."
            )

        try:
            prompt = self._build_prompt(message, context, history or [])
            print(f"Generating response with device: {self.device}")
            print(f"Prompt: {prompt[:200]}...")

            with self.model.chat_session():
                response = self.model.generate(
                    prompt,
                    max_tokens=500,
                    temp=0.7,
                    top_k=40,
                    top_p=0.9,
                    repeat_penalty=1.1,
                )

            print(f"Response generated: {len(response)} chars")
            return response.strip()
        except Exception as e:
            print(f"Generation error: {e}")
            import traceback
            traceback.print_exc()
            return f"Error generating response: {str(e)}"
    
    def _build_prompt(self, message: str, context: str, history: List[Dict]) -> str:
        """Build a prompt with context and conversation history"""
        prompt_parts = []
        
        # Add context
        if context:
            prompt_parts.append(f"Context:\n{context}\n")
        
        # Add conversation history (last 5 exchanges)
        if history:
            prompt_parts.append("Conversation History:")
            for entry in history[-10:]:  # Last 5 exchanges (10 messages)
                role = entry['role'].capitalize()
                content = entry['content']
                prompt_parts.append(f"{role}: {content}")
            prompt_parts.append("")
        
        # Add current message
        prompt_parts.append(f"User: {message}")
        prompt_parts.append("Assistant:")
        
        return "\n".join(prompt_parts)
    
    def is_model_loaded(self) -> bool:
        """Check if model is loaded"""
        return self.model is not None

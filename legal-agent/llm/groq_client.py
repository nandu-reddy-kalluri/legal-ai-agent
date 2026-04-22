"""
llm/groq_client.py
------------------
Groq LLM client wrapper using currently supported models (April 2026).
Includes automatic fallback chain for model deprecation.

Supported models (as of April 2026):
  - llama-3.3-70b-versatile   (best quality, primary)
  - llama-3.1-8b-instant      (fast, fallback)
"""

import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# ── Model fallback chain (ordered best → fastest) ─────────────────────────────
MODEL_CHAIN = [
    "llama-3.3-70b-versatile",   # Best quality - primary
    "llama-3.1-8b-instant",      # Fast fallback
]

DEFAULT_MODEL = MODEL_CHAIN[0]


class GroqClient:
    """Thin wrapper around the Groq API with automatic model fallback."""

    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.2):
        self.model_choice = os.environ.get("CURRENT_MODEL_CHOICE", "Groq (Cloud)")
        
        if self.model_choice == "Groq (Cloud)":
            api_key = os.environ.get("GROQ_API_KEY") or GROQ_API_KEY
            if not api_key:
                raise EnvironmentError("GROQ_API_KEY not set in .env or settings")
            self.client      = Groq(api_key=api_key)
            self.model       = model
        else:
            self.client      = None
            self.model       = "llama3"
            
        self.temperature = temperature

    def _call_with_fallback(self, messages: list, max_tokens: int) -> str:
        if self.model_choice == "Local (Ollama)":
            return self._call_ollama(messages)

        """Try the current model, then walk through the fallback chain."""
        # Build ordered list: current model first, then remaining chain models
        models_to_try = [self.model] + [m for m in MODEL_CHAIN if m != self.model]

        last_error = None
        for model_id in models_to_try:
            try:
                response = self.client.chat.completions.create(
                    model=model_id,
                    temperature=self.temperature,
                    max_tokens=max_tokens,
                    messages=messages,
                )
                # If we switched models, persist the working one
                if model_id != self.model:
                    print(f"[groq_client] Switched from '{self.model}' → '{model_id}'")
                    self.model = model_id
                return response.choices[0].message.content
            except Exception as e:
                last_error = e
                err_str = str(e).lower()
                if "decommissioned" in err_str or "model" in err_str or "not found" in err_str:
                    print(f"[WARNING] Model '{model_id}' unavailable: {e}")
                    continue  # try next model in chain
                else:
                    raise  # non-model error, raise immediately

        # All models failed
        raise RuntimeError(
            f"All models exhausted. Last error: {last_error}\n"
            f"Tried: {models_to_try}"
        )

    def generate(self, system_prompt: str, user_prompt: str, max_tokens: int = 4096) -> str:
        """Send a chat completion request and return the response text."""
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]
        return self._call_with_fallback(messages, max_tokens)

    def generate_simple(self, prompt: str, max_tokens: int = 4096) -> str:
        """Single-turn generation without explicit system/user split."""
        messages = [{"role": "user", "content": prompt}]
        return self._call_with_fallback(messages, max_tokens)

    def _call_ollama(self, messages: list) -> str:
        import requests
        
        system_prompt = ""
        prompt = ""
        for m in messages:
            if m["role"] == "system":
                system_prompt += m["content"] + "\n"
            else:
                prompt += m["content"] + "\n"
                
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={
                    "model": "llama3",
                    "prompt": prompt.strip(),
                    "system": system_prompt.strip(),
                    "stream": False
                }
            )
            return response.json()["response"]
        except Exception as e:
            raise RuntimeError(f"Ollama request failed: {e}. Make sure Ollama is running.")

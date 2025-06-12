import subprocess
from typing import Optional


def generate_hypothesis(prompt: str, model: str = 'llama3') -> str:
    """Generate a hypothesis using a local LLM via Ollama.

    Falls back to a placeholder response if Ollama is not available."""
    cmd = ['ollama', 'run', model, prompt]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception:
        return f"[Simulated output for model '{model}'] Hypothesis about: {prompt}"

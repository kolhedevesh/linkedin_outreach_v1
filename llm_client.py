import requests
import json
import logging

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def query_llama(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=10)
    except Exception as e:
        logger.exception("Error contacting Ollama server")
        raise RuntimeError(f"LLM request failed: {e}")

    if response.status_code != 200:
        logger.error("Ollama returned non-200: %s %s", response.status_code, response.text)
        raise RuntimeError(f"LLM error: {response.status_code} - {response.text}")

    try:
        data = response.json()
    except Exception:
        logger.error("Failed to parse JSON from Ollama response: %s", response.text)
        raise RuntimeError("Invalid JSON response from LLM")

    # Ollama outputs may have different keys depending on the server/mode.
    # Try common keys, otherwise return the raw text field if present.
    for key in ("response", "text", "result", "output"):
        if key in data:
            return data.get(key) or ""

    # As a last resort, return the whole payload as string
    return json.dumps(data)

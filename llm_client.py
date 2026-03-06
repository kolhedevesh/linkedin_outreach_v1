import json
import logging
import os
import streamlit as st
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_groq_api_key() -> str:
    try:
        value = st.secrets["GROQ_API_KEY"]
    except Exception:
        value = os.getenv("GROQ_API_KEY")
    if not value:
        raise ValueError("Missing API key in Streamlit secrets")
    return value


def query_llama(prompt: str, temperature: float = 0.7, max_output_tokens: int = 180) -> str:
    logger.info("Using Groq LLM")
    print("Using Groq LLM")
    api_key = get_groq_api_key()
    client = Groq(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_output_tokens,
        )
    except Exception as e:
        logger.exception("Groq request failed")
        raise RuntimeError(f"LLM request failed: {e}")

    try:
        return completion.choices[0].message.content
    except Exception:
        return json.dumps(completion)

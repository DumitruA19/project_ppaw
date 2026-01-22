# app/core/openai_client.py
from __future__ import annotations
from typing import Iterable, List, Optional, Dict, Generator
import time
from openai import OpenAI
from sentence_transformers import SentenceTransformer # Pentru embeddings moca
from app.core.config import get_settings

settings = get_settings()

# 🚀 Clientul Groq (Folosește cheia ta din .env)
_groq_client = OpenAI(
    api_key=settings.GROQ_API_KEY, 
    base_url="https://api.groq.com/openai/v1"
)

# 🧠 Model local gratuit pentru Embeddings (înlocuiește OpenAI text-embedding-3-small)
# Se descarcă automat la prima rulare (aprox 100MB)
_embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# -------- embeddings (MOCA & LOCAL) --------
def embed(texts: Iterable[str]) -> List[List[float]]:
    """
    Generează vectori local, fără a apela un API extern.
    Acest lucru face ca retriever.similar din chat_service să funcționeze.
    """
    texts = [t if isinstance(t, str) else str(t) for t in texts]
    if not texts:
        return []
    
    # Generăm embeddings folosind procesorul local
    embeddings = _embed_model.encode(texts)
    return embeddings.tolist()

# -------- chat (GROQ ONLY) --------
def chat_complete(messages: List[Dict], temperature: float = 0.2) -> Dict:
    """
    Folosește exclusiv Groq. Am eliminat formatul 'responses' care era specific OpenAI.
    """
    t0 = time.time()
    
    # Groq folosește formatul standard Chat Completions
    resp = _groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile", # Cel mai capabil model gratuit de pe Groq
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
    )
    
    dt = int((time.time() - t0) * 1000)
    usage = getattr(resp, "usage", None)
    
    return {
        "text": (resp.choices[0].message.content or "").strip(),
        "usage": {
            "input_tokens": getattr(usage, "prompt_tokens", 0),
            "output_tokens": getattr(usage, "completion_tokens", 0),
        },
        "latency_ms": dt,
    }

# -------- chat streaming (SSE) --------
def chat_complete_stream(messages: List[Dict], temperature: float = 0.2) -> Generator[str, None, None]:
    """Generator pentru streaming compatibil cu Groq."""
    stream = _groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=temperature,
        max_tokens=1024,
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content
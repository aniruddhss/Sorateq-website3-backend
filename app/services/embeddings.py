import logging
import hashlib
import numpy as np
from typing import List
from app.core.config import settings

logger = logging.getLogger(__name__)

# Cache clients
_openai_client = None
_gemini_client = None

def get_openai_client():
    global _openai_client
    if _openai_client is None and settings.OPENAI_API_KEY:
        try:
            from openai import AsyncOpenAI
            _openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        except Exception as e:
            logger.warning(f"Could not init OpenAI client: {e}")
    return _openai_client


def get_gemini_client():
    global _gemini_client
    if _gemini_client is None and settings.GEMINI_API_KEY:
        try:
            from google import genai
            _gemini_client = genai.Client(api_key=settings.GEMINI_API_KEY)
        except Exception as e:
            logger.warning(f"Could not init Gemini client: {e}")
    return _gemini_client


async def get_embedding(text: str) -> List[float]:
    """
    Generate 1536-dim embedding using Gemini (gemini-embedding-001) or OpenAI (text-embedding-3-small).
    Falls back to deterministic normalized pseudo-vector if API keys are not configured.
    """
    # 1. Try Gemini
    gemini_client = get_gemini_client()
    if gemini_client:
        try:
            from google.genai import types
            result = gemini_client.models.embed_content(
                model=getattr(settings, "EMBEDDING_MODEL", "gemini-embedding-001"),
                contents=text[:8000],
                config=types.EmbedContentConfig(output_dimensionality=1536)
            )
            vec = result.embeddings[0].values
            if len(vec) == 1536:
                return vec
            elif len(vec) < 1536:
                return vec + [0.0] * (1536 - len(vec))
            else:
                return vec[:1536]
        except Exception as e:
            logger.warning(f"Gemini embedding fallback: {e}")

    # 2. Try OpenAI (only if a valid non-placeholder key is provided)
    if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("your-"):
        openai_client = get_openai_client()
        if openai_client:
            try:
                response = await openai_client.embeddings.create(
                    input=[text[:8000]],
                    model="text-embedding-3-small"
                )
                return response.data[0].embedding
            except Exception as e:
                logger.error(f"OpenAI embedding error: {e}")

    # 3. Deterministic fallback pseudo-vector (1536 floats)
    h = hashlib.sha256(text.encode("utf-8")).digest()
    np.random.seed(int.from_bytes(h[:4], "little"))
    vec = np.random.randn(1536).astype(float)
    norm = np.linalg.norm(vec)
    if norm > 0:
        vec = vec / norm
    return vec.tolist()


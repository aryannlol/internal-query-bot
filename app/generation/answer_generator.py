import httpx
import logging
from app.utils.prompts import SYSTEM_PROMPT
from app.config import settings

logger = logging.getLogger(__name__)
class AnswerGenerator:
    async def generate(self, query: str, retrieved_chunks: list, history: list = None):
        # 1. Format Chat History first so we have it available
        chat_context = ""
        if history:
            for msg in history[-5:]:
                role = getattr(msg, 'role', msg.get('role') if isinstance(msg, dict) else "")
                content = getattr(msg, 'content', msg.get('content') if isinstance(msg, dict) else "")
                role_label = "User" if role == "user" else "Assistant"
                chat_context += f"{role_label}: {content}\n"

        # 2. FIXED: Allow the bot to proceed if there is history, even if chunks are empty
        if not retrieved_chunks and not chat_context:
            return {
                "answer": "I do not have enough information to answer this.",
                "sources": [],
                "confidence": "Low"
            }

        # 3. Limit chunks
        chunks = retrieved_chunks[:settings.max_chunks] if retrieved_chunks else []

        # 4. Build context string
        context = "\n\n".join(
            f"[Source: {c['source']}]\n{c['content'][:settings.max_chars_per_chunk]}"
            for c in chunks
        )

        # 5. The Prompt (Stayed the same, but now it actually gets reached!)
        # In app/generation/answer_generator.py, update the prompt variable:
        prompt = f"""{SYSTEM_PROMPT}

Below is the data you must use to answer. Do not include these labels in your response.

CONVERSATION HISTORY:
{chat_context if chat_context else "None"}

DOCUMENT CONTEXT:
{context}

CURRENT USER REQUEST: 
{query}

FINAL INSTRUCTION: Provide the answer in the requested style. If no style is requested, be professional.
"""
        payload = {
            "model": settings.ollama_model,
            "prompt": prompt,
            "stream": False
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    settings.ollama_url,
                    json=payload,
                    timeout=settings.ollama_timeout
                )
                response.raise_for_status()
                output = response.json().get("response", "").strip()

        except httpx.TimeoutException:
            logger.error(f"Ollama timeout for query: {query[:50]}...")
            return {"answer": "The system took too long to generate an answer.", "sources": [], "confidence": "Low"}
        
        except httpx.HTTPStatusError as e:
            logger.error(f"Ollama HTTP error: {e.response.status_code}")
            return {"answer": "The system encountered an error generating the answer.", "sources": [], "confidence": "Low"}
        
        except httpx.ConnectError:
            logger.error("Cannot connect to Ollama - is it running?")
            return {"answer": "The system is temporarily unavailable. Please try again later.", "sources": [], "confidence": "Low"}
        
        except Exception as e:
            logger.error(f"Unexpected error in LLM generation: {e}")
            return {"answer": "An unexpected error occurred.", "sources": [], "confidence": "Low"}

        # 6. Final formatting of response
        sources = list({c["source"] for c in chunks})
        confidence = self._calculate_confidence(output, chunks)

        return {
            "answer": output,
            "sources": sources,
            "confidence": confidence
        }

    def _calculate_confidence(self, output: str, chunks: list) -> str:
        output_lower = output.lower()
        
        if any(phrase in output_lower for phrase in [
            "do not have enough information",
            "cannot answer",
            "insufficient information",
            "not clear from the context"
        ]):
            return "Low"
        
        if len(chunks) >= 3 and any(word in output_lower for word in ["according to", "states that", "specifies"]):
            return "High"
        
        if len(chunks) >= 2:
            return "Medium"
        
        return "Low"
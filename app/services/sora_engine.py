import json
import logging
import re
from typing import AsyncGenerator, Dict, Any, List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.config import settings
from app.services.rag_service import RAGService
from app.services.intent_classifier import IntentClassifier

logger = logging.getLogger(__name__)

def intent_hint(message: str) -> Optional[str]:
    """Return a short project-type label when the visitor names one, so the stage machine can skip discovery."""
    lower = message.lower()
    for label, words in (
        ("RAG or AI chatbot", ("rag", "chatbot", "ai assistant", "llm")),
        ("website", ("website", "web site", "landing page", "portfolio site")),
        ("SaaS platform", ("saas", "dashboard", "subscription")),
        ("mobile app", ("mobile app", "ios app", "android app")),
        ("automation", ("automate", "automation", "workflow")),
    ):
        if any(w in lower for w in words):
            return label
    return None


# Must match CONTACT_OPTIONS_AFTER_TURNS in src/lib/sora/policy.ts
CONTACT_OPTIONS_AFTER_TURNS = 3

SORA_SYSTEM_PROMPT = """You are Sora, the AI sales consultant for Sorateq, a product engineering studio.

## GOAL
Understand what the visitor wants to build, show relevant Sorateq experience, suggest a preliminary approach, and offer a meeting or callback. You are a helpful consultant, not a form.

## CURRENT STAGE
{stage_instruction}

## RULES (follow strictly)
1. Understand before selling: take the project type and intended outcome from what the visitor already said. Never ask them to re-explain or define a term they used.
2. Every question must earn its place: ask only if the answer changes the solution, feasibility, or initial scope. Ask ONE question per reply. Never exceed 4 discovery questions in the whole conversation. Never ask about anything already stated in the conversation.
3. Acknowledge, then add value: briefly reflect what they said and connect it to something Sorateq can offer. Do not repeat their words back, flatter, or ask a new question every time.
4. Use company knowledge as evidence: mention only projects, capabilities, technologies and examples present in the CONTEXT below, and only where they relate to the visitor's idea. Never invent a past project, client, result, technology competency, URL, or guarantee. If nothing relevant exists, say so plainly and do not cite anything.
5. Useful initial approach: when enough context exists, describe the likely solution at a high level. Frame architecture and estimates as preliminary, not a final proposal. Never quote prices unless the CONTEXT contains them and the visitor asked.
6. Earn the meeting: offer the meeting or callback after you have shown understanding and a useful overview. If the visitor asks to book, offer it immediately.
7. Keep it conversational: 2 to 3 sentences per reply, never more than 4. No bullet points, headers, bold, emojis, or filler ("Great!", "Excited to help!"). No technical dumps and no repeated summaries.
8. Always end with exactly one of: one question, or one clear next step. Never end with a bare statement.
9. Stay on the visitor's topic. If they correct you or say you misunderstood, acknowledge the correction in one sentence and continue from their correction.

## CONTEXT (use only when relevant to what the visitor said)
{retrieved_context}

## CONVERSATION STATE
{system_state}

Speak like a sharp, honest senior consultant. Be brief, specific, and useful.
"""


class SoraEngine:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.rag = RAGService(db)

    async def generate_response_stream(
        self,
        message: str,
        conversation_history: List[Dict[str, Any]],
        current_profile: Dict[str, Any],
        current_state: str,
        question_count: int = 0,
    ) -> AsyncGenerator[str, None]:
        """
        Orchestrates intent detection, hybrid RAG retrieval, prompt assembly, and SSE streaming.
        Passes full conversation history to the LLM for proper context retention.
        """
        # 1. Intent classification & profile extraction
        intent, confidence = IntentClassifier.classify_intent(message)
        updated_profile = IntentClassifier.extract_project_fields(message, current_profile)
        new_state = IntentClassifier.transition_state(current_state, intent, updated_profile)

        # 2. Hybrid RAG retrieval (Strict PUBLIC visibility)
        relevant_projects = await self.rag.search_projects(
            query=f"{message} {updated_profile.get('industry', '')}",
            limit=3,
            visibility="PUBLIC"
        )
        relevant_knowledge = await self.rag.search_knowledge(
            query=message,
            limit=3,
            visibility="PUBLIC"
        )

        # Build context block (kept minimal so LLM focuses on conversation)
        context_parts = []
        if relevant_projects:
            context_parts.append("### Relevant Sorateq Projects (use only if visitor asks):")
            for p in relevant_projects:
                context_parts.append(
                    f"- {p['name']} ({p['industry']}): {p['summary']}"
                )
        if relevant_knowledge:
            context_parts.append("\n### Sorateq Capabilities:")
            for k in relevant_knowledge:
                context_parts.append(f"- {k['title']}: {k['content']}")

        retrieved_context = "\n".join(context_parts) if context_parts else "Sorateq builds websites, SaaS platforms, mobile apps, AI integrations, and custom software."

        # Build structured state for the LLM
        known = {}
        if updated_profile.get("industry"):
            known["industry"] = updated_profile["industry"]
        if updated_profile.get("problem_statement"):
            known["what_they_want"] = updated_profile["problem_statement"]
        if updated_profile.get("target_audience"):
            known["target_audience"] = updated_profile["target_audience"]
        if updated_profile.get("timeline"):
            known["timeline"] = updated_profile["timeline"]

        # Stage selection (fixed state machine, decided in code rather than by the LLM)
        known_signals = {
            "project_type": updated_profile.get("project_category") or updated_profile.get("project_name") or intent_hint(message),
            "outcome": updated_profile.get("problem_statement") or updated_profile.get("solution"),
            "audience": updated_profile.get("target_audience") or updated_profile.get("users"),
            "timeline": updated_profile.get("timeline"),
        }
        asks_to_book = bool(re.search(r"\b(book|schedule|call me|callback|call back|meeting|talk to (a|your) (human|team|someone))\b", message, re.I))
        discovery_questions_asked = question_count
        options_visible = question_count >= CONTACT_OPTIONS_AFTER_TURNS

        if asks_to_book or options_visible:
            stage = "offer_next_step"
            stage_instruction = (
                "Stage 5, offer the next step. Briefly summarize the likely approach in one sentence, then say 'Choose an option below to schedule a call, send an email, or request a callback.' Do not ask another question."
            )
        elif known_signals["project_type"] and not known_signals["audience"] and discovery_questions_asked < 2:
            stage = "clarify"
            stage_instruction = (
                "Stage 2, clarify. You already know what they want to build. Ask ONE question only if it changes the solution (for example, who will use it). Reflect their idea in one sentence first. Do not ask about anything in CONVERSATION STATE."
            )
        elif known_signals["project_type"] and known_signals["audience"]:
            stage = "show_expertise_and_approach"
            stage_instruction = (
                "Stage 3 and 4, show relevant expertise and suggest a preliminary approach. Use CONTEXT only where it relates to their idea. Describe the likely solution at a high level and label it preliminary. End with one question or the next step."
            )
        else:
            stage = "understand"
            stage_instruction = (
                "Stage 1, understand. Ask what they want to build, in one plain question. Do not assume a product type."
            )

        known = {k: v for k, v in known_signals.items() if v}
        system_state = {
            "stage": stage,
            "discovery_questions_asked": discovery_questions_asked,
            "max_discovery_questions": 4,
            "contact_options_visible": options_visible,
            "known_about_project": known,
        }

        # Format system prompt
        formatted_system_prompt = SORA_SYSTEM_PROMPT.format(
            stage_instruction=stage_instruction,
            retrieved_context=retrieved_context,
            system_state=json.dumps(system_state, indent=2),
        )

        cta_ready = stage == "offer_next_step"
        # Yield metadata event first
        meta_event = {
            "type": "meta",
            "intent": intent,
            "confidence": confidence,
            "state": new_state,
            "project_profile": updated_profile,
            "relevant_projects": relevant_projects,
            "cta_ready": cta_ready,
            "stage": stage,
        }
        yield f"data: {json.dumps(meta_event)}\n\n"

        streaming_done = False

        # Build conversation messages for multi-turn context
        llm_messages = [{"role": "system", "content": formatted_system_prompt}]
        for turn in (conversation_history or []):
            role = turn.get("role") or turn.get("sender", "user")
            if role == "assistant":
                role = "model"  # Gemini uses 'model'
            content = turn.get("content", "")
            if content:
                llm_messages.append({"role": role, "content": content})
        llm_messages.append({"role": "user", "content": message})

        # 1. Try Google Gemini with full conversation history (using installed google-genai SDK)
        if settings.GEMINI_API_KEY and not streaming_done:
            try:
                from google import genai
                from google.genai import types as genai_types

                client = genai.Client(api_key=settings.GEMINI_API_KEY)
                model_name = getattr(settings, "GEMINI_MODEL", "gemini-1.5-flash")

                # Build contents array with full history for multi-turn context
                contents = []
                for turn in (conversation_history or []):
                    role = turn.get("role") or turn.get("sender", "user")
                    content = turn.get("content", "")
                    if content:
                        gemini_role = "model" if role == "assistant" else "user"
                        contents.append(genai_types.Content(
                            role=gemini_role,
                            parts=[genai_types.Part(text=content)]
                        ))
                # Append current user message
                contents.append(genai_types.Content(
                    role="user",
                    parts=[genai_types.Part(text=message)]
                ))

                response_stream = client.models.generate_content_stream(
                    model=model_name,
                    contents=contents,
                    config=genai_types.GenerateContentConfig(
                        system_instruction=formatted_system_prompt,
                        temperature=0.3,
                        max_output_tokens=200,
                    )
                )
                for chunk in response_stream:
                    if chunk.text:
                        clean_text = chunk.text.replace("**", "").replace("*", "")
                        yield f"data: {json.dumps({'type': 'token', 'token': clean_text})}\n\n"
                streaming_done = True
            except Exception as e:
                logger.error(f"Gemini streaming error: {e}. Trying OpenAI fallback.")

        # 2. Try OpenAI with full conversation history
        if settings.OPENAI_API_KEY and not settings.OPENAI_API_KEY.startswith("your-") and not streaming_done:
            try:
                from openai import AsyncOpenAI
                client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

                openai_messages = [{"role": "system", "content": formatted_system_prompt}]
                for turn in (conversation_history or []):
                    role = turn.get("role") or turn.get("sender", "user")
                    if role == "assistant":
                        role = "assistant"
                    content = turn.get("content", "")
                    if content:
                        openai_messages.append({"role": role, "content": content})
                openai_messages.append({"role": "user", "content": message})

                stream = await client.chat.completions.create(
                    model=settings.ROUTING_PRIMARY_MODEL,
                    messages=openai_messages,
                    stream=True,
                    temperature=0.3,
                    max_tokens=200
                )
                async for chunk in stream:
                    delta = chunk.choices[0].delta.content or ""
                    if delta:
                        clean_delta = delta.replace("**", "").replace("*", "")
                        yield f"data: {json.dumps({'type': 'token', 'token': clean_delta})}\n\n"
                streaming_done = True
            except Exception as e:
                logger.error(f"OpenAI streaming error: {e}. Falling back to deterministic engine.")

        # 3. Deterministic fallback
        if not streaming_done:
            fallback_text = self._build_deterministic_response(
                message=message,
                intent=intent,
                profile=updated_profile,
                state=new_state,
                question_count=question_count,
                conversation_history=conversation_history or []
            )
            words = fallback_text.split(" ")
            for i in range(0, len(words), 3):
                chunk = " ".join(words[i:i+3]) + (" " if i+3 < len(words) else "")
                yield f"data: {json.dumps({'type': 'token', 'token': chunk})}\n\n"

        yield f"data: {json.dumps({'type': 'done'})}\n\n"

    def _build_deterministic_response(
        self,
        message: str,
        intent: str,
        profile: Dict[str, Any],
        state: str,
        question_count: int,
        conversation_history: List[Dict[str, Any]]
    ) -> str:
        """
        Content-aware fallback. Reads the actual message and history to respond appropriately.
        NEVER uses question_count as a trigger for price — only when truly qualified.
        """
        msg = message.lower()
        history_text = " ".join(t.get("content", "") for t in conversation_history if t.get("role") != "assistant").lower()
        combined = f"{history_text} {msg}".strip()

        # Always-respond intents
        if intent == "pricing" or any(w in msg for w in ["cost", "price", "how much", "budget"]):
            return "Cost depends heavily on scope — choose an option below and we'll give you an exact number after a 25-minute call."

        if intent == "meeting" or "call" in msg or "schedule" in msg:
            return "Let's make that happen — choose an option below to book a quick session with our team."

        # Qualification check: do we know enough to recommend + price?
        known_signals = [
            profile.get("industry"),
            profile.get("target_audience"),
            profile.get("problem_statement"),
            profile.get("platform"),
        ]
        sufficiently_known = sum(1 for s in known_signals if s) >= 2
        
        if sufficiently_known and question_count >= 1:
            # We know enough — give a contextual recommendation
            if "automate" in combined:
                return f"Based on what you've described, this sounds like a workflow automation project. Choose an option below to schedule a call, send an email, or request a callback for an exact quote."
            elif "saas" in combined or "platform" in combined:
                return f"This sounds like a solid SaaS product to build. Choose an option below to schedule a call, send an email, or request a callback for an exact quote."
            else:
                industry = profile.get("industry", "")
                label = f"for {industry}" if industry else ""
                return f"From what you've described, you need a professional digital product {label}. Choose an option below and we'll scope it out exactly."

        # --- Discovery questions (content-matched, never generic) ---
        if "automate" in combined or "automation" in combined:
            if "process" in combined or "workflow" in combined:
                return "What does that process look like today, and where does it break down?"
            return "What specific task or process are you trying to eliminate or speed up?"

        if "saas" in combined or "platform" in combined:
            if profile.get("target_audience"):
                return "What is the core workflow users need to complete inside it?"
            return "Who are the primary users of this product?"

        if "website" in combined:
            if profile.get("target_audience"):
                return "What is the main action you want visitors to take when they land on it?"
            return "What is the main goal of the site — building trust, getting leads, or selling directly?"

        if "app" in combined or "mobile" in combined:
            return "Who is this for, and what is the one thing you want them to do in the app?"

        # Truly vague — ask one open question
        return "What problem are you trying to solve, or what do you want the product to help people do?"

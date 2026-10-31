import re
import json
import logging
from typing import Dict, Any, Tuple

logger = logging.getLogger(__name__)

INTENT_KEYWORDS = {
    "meeting": ["call", "meet", "schedule", "talk to human", "book", "zoom", "calendly", "consultation", "founder"],
    "portfolio": ["portfolio", "projects", "work", "built", "examples", "case study", "show me", "reference", "apps"],
    "pricing": ["pricing", "cost", "how much", "rate", "quote", "budget", "expensive", "fee", "retainer"],
    "timeline": ["timeline", "how long", "delivery", "weeks", "turnaround", "deadline", "fast"],
    "capabilities": ["capabilities", "services", "ai", "mobile", "full stack", "what do you do", "mvp", "backend"],
    "methodology": ["process", "methodology", "how do you work", "agile", "sprint", "steps", "workflow"],
    "company": ["what is sorateq", "who are you", "team", "founder", "about sorateq", "where are you based", "history"],
    "technology": ["tech stack", "fastapi", "nextjs", "python", "postgres", "supabase", "react native", "technologies"],
    "project_inquiry": ["i want to build", "building", "my idea", "saas", "app", "platform", "looking for developer", "develop", "mvp", "startup"]
}

VALID_STATES = [
    "NEW",
    "INTRODUCTION",
    "GENERAL_DISCOVERY",
    "PROJECT_DISCOVERY",
    "PROJECT_DEFINITION",
    "QUALIFICATION",
    "PORTFOLIO_EXPLORATION",
    "PROJECT_PLANNING",
    "PRICING_DISCUSSION",
    "MEETING_INTENT",
    "BOOKING",
    "COMPLETED"
]


class IntentClassifier:
    @staticmethod
    def classify_intent(message: str) -> Tuple[str, int]:
        """
        Lightweight deterministic intent classifier.
        Returns (intent_name, confidence_percentage).
        """
        msg_lower = message.lower()
        scores = {}
        for intent, kws in INTENT_KEYWORDS.items():
            match_count = sum(1 for kw in kws if kw in msg_lower)
            if match_count > 0:
                scores[intent] = match_count

        if not scores:
            if len(message.split()) > 6:
                return ("project_inquiry", 60)
            return ("clarification", 50)

        best_intent = max(scores, key=scores.get)
        confidence = min(95, 50 + scores[best_intent] * 20)
        return (best_intent, confidence)

    @staticmethod
    def extract_project_fields(message: str, current_profile: Dict[str, Any]) -> Dict[str, Any]:
        """
        Progressively extract project attributes without hallucinations or interrogating.
        """
        msg = message.lower()
        updated = dict(current_profile or {})

        # Industry heuristics
        industries = {
            "health": "HealthTech & Healthcare",
            "medical": "HealthTech & Medical",
            "fintech": "FinTech & Financial Services",
            "crypto": "FinTech & Web3",
            "finance": "FinTech",
            "edtech": "EdTech & Education",
            "school": "EdTech & Campus Management",
            "education": "EdTech",
            "logistics": "Logistics & Supply Chain",
            "fleet": "Logistics & Fleet Ops",
            "construction": "ConTech & Field Management",
            "security": "Cybersecurity & Governance",
            "compliance": "Compliance & Audit SaaS",
            "ecommerce": "E-Commerce & Retail",
            "retail": "E-Commerce",
            "video": "AI Video & Creative Tools",
            "crm": "SalesTech & CRM"
        }
        for kw, ind in industries.items():
            if kw in msg and not updated.get("industry"):
                updated["industry"] = ind
                break

        # Platform heuristics
        if "mobile" in msg or "ios" in msg or "android" in msg:
            updated["platform"] = "Mobile (iOS & Android) + Web"
        elif "web" in msg or "saas" in msg:
            if not updated.get("platform"):
                updated["platform"] = "Web Application / SaaS"

        # AI Requirements
        if any(w in msg for w in ["ai", "llm", "rag", "agents", "gemini", "gpt", "vision"]):
            updated["ai_requirements"] = "Generative AI / RAG / Agentic Workflows"

        # Timeline
        timeline_match = re.search(r'(\d+[\s-]*(?:week|month|day)s?)', msg)
        if timeline_match:
            updated["timeline"] = timeline_match.group(1)

        # Budget
        budget_match = re.search(r'(\$[\d,]+|\d+k|\d+\s*(?:usd|dollars|inr|eur))', msg)
        if budget_match:
            updated["budget"] = budget_match.group(1)

        # Problem/Solution inference if user speaks of building
        if "i want to build" in msg or "we are building" in msg or "looking to create" in msg:
            if not updated.get("problem_statement"):
                updated["problem_statement"] = message.strip()
            if not updated.get("solution"):
                updated["solution"] = message.strip()

        return updated

    @staticmethod
    def transition_state(current_state: str, intent: str, profile: Dict[str, Any]) -> str:
        """
        Deterministic conversation state machine.
        """
        if intent == "meeting":
            return "MEETING_INTENT"
        if intent == "portfolio":
            return "PORTFOLIO_EXPLORATION"
        if intent == "pricing":
            return "PRICING_DISCUSSION"
        
        if current_state == "NEW":
            return "PROJECT_DISCOVERY" if intent == "project_inquiry" else "GENERAL_DISCOVERY"
        elif current_state == "PROJECT_DISCOVERY":
            if profile.get("industry") or profile.get("platform"):
                return "PROJECT_DEFINITION"
            return "PROJECT_DISCOVERY"
        elif current_state == "PROJECT_DEFINITION":
            if profile.get("timeline") or profile.get("budget") or profile.get("ai_requirements"):
                return "PROJECT_PLANNING"
            return "PROJECT_DEFINITION"
        elif current_state == "PROJECT_PLANNING":
            return "QUALIFICATION"

        return current_state or "PROJECT_DISCOVERY"

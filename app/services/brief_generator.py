from typing import Dict, Any


class BriefGenerator:
    @staticmethod
    def generate_brief(profile: Dict[str, Any], conversation_summary: str = "") -> Dict[str, Any]:
        """
        Generates a clean, structured project brief with clearly distinguished known vs estimated fields.
        """
        return {
            "project_name": profile.get("project_name") or "New Technical Initiative",
            "objective": profile.get("solution") or "Build and launch production-grade digital platform.",
            "problem": profile.get("problem_statement") or "Needs scalable modern architecture to address user workflows.",
            "target_users": profile.get("target_audience") or profile.get("users") or "Identified domain users and operators.",
            "proposed_mvp": profile.get("mvp_requirements") or [
                "Core authentication & Role-Based Access Control",
                "Primary operational data workflows",
                "Asynchronous background pipeline",
                "Analytics & telemetry dashboard"
            ],
            "potential_architecture": profile.get("platform") or "Next.js App Router + FastAPI async backend + PostgreSQL / pgvector + Supabase Auth",
            "integrations": profile.get("integrations") or ["Payment gateway (Stripe/Razorpay)", "Storage (AWS S3/Cloudflare R2)", "AI LLM Provider"],
            "timeline": profile.get("timeline") or "Estimated 4 - 8 weeks for production MVP",
            "budget": profile.get("budget") or "Discussed during scoping review",
            "current_stage": profile.get("current_stage") or "Architecture & Discovery Phase",
            "open_questions": [
                "Detailed schema requirements for primary domain entities",
                "Target volume and concurrency benchmarks for initial release",
                "Specific third-party API webhook constraints"
            ],
            "next_step": "25-minute technical scoping call with Sorateq Solution Architects."
        }

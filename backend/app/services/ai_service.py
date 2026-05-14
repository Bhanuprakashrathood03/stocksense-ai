import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage

from ..core.config import settings
from ..models.chat import ChatHistory


class AIService:
    def __init__(self, user, db: AsyncSession):
        self.user = user
        self.db = db
        self.llm = self._get_llm()

    def _get_llm(self):
        if settings.llm_provider == "ollama":
            return ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.3)
        return ChatOpenAI(
            model=settings.llm_model,
            temperature=0.3,
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url,
        )

    def _system_prompt(self) -> str:
        return f"""You are StockSense AI, a professional stock market assistant.
User plan: {self.user.plan.value}
Provide concise, data-driven insights. For free tier: basic analysis only.
For pro: detailed technical analysis, fundamentals, and recommendations.
For enterprise: all features plus portfolio optimization and risk analysis.
Always include disclaimers."""

    async def chat(self, message: str, session_id: Optional[str] = None) -> tuple[str, str]:
        if not session_id:
            session_id = str(uuid.uuid4())
        messages = [SystemMessage(content=self._system_prompt()), HumanMessage(content=message)]
        result = await self.llm.ainvoke(messages)
        response = result.content
        await self._save_message(session_id, "user", message, result.usage_metadata.get("input_tokens", 0) if hasattr(result, "usage_metadata") else 0)
        await self._save_message(session_id, "assistant", response, result.usage_metadata.get("output_tokens", 0) if hasattr(result, "usage_metadata") else 0)
        return response, session_id

    async def _save_message(self, session_id: str, role: str, content: str, tokens: int = 0):
        msg = ChatHistory(user_id=self.user.id, session_id=session_id, role=role, content=content, tokens_used=tokens)
        self.db.add(msg)
        await self.db.flush()

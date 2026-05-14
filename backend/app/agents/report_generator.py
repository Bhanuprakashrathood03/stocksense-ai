import uuid
from datetime import datetime, timezone
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.config import settings
from ..models.chat import AIReport
from ..models.portfolio import Portfolio, Holding


class ReportGenerator:
    def __init__(self):
        if settings.llm_provider == "ollama":
            self.llm = ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.3)
        else:
            self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.3, api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def generate(self, user_id: str, report_type: str, db: AsyncSession) -> dict:
        result = await db.execute(select(Portfolio).where(Portfolio.user_id == user_id))
        portfolios = result.scalars().all()
        context = f"User has {len(portfolios)} portfolios. "
        for p in portfolios:
            h_result = await db.execute(select(Holding).where(Holding.portfolio_id == p.id))
            holdings = h_result.scalars().all()
            context += f"Portfolio '{p.name}': {len(holdings)} holdings, value {p.total_value}. "

        messages = [
            SystemMessage(content=f"Generate a {report_type} report. Return structured markdown."),
            HumanMessage(content=f"Generate a {report_type} report based on: {context}. Include summary, analysis, recommendations."),
        ]
        result = await self.llm.ainvoke(messages)
        content = result.content
        report = AIReport(
            user_id=user_id,
            type=report_type,
            title=f"{report_type.replace('_', ' ').title()} - {datetime.now(timezone.utc).strftime('%Y-%m-%d')}",
            content=content,
        )
        db.add(report)
        await db.flush()
        return {"id": report.id, "type": report.type, "title": report.title, "content": content, "created_at": report.created_at}

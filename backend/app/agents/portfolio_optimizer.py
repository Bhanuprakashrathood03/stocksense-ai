from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.config import settings
from ..models.portfolio import Holding, Portfolio


class PortfolioOptimizerAgent:
    def __init__(self):
        if settings.llm_provider == "ollama":
            self.llm = ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.2)
        else:
            self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.2, api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def optimize(self, user_id: str, db: AsyncSession) -> dict:
        result = await db.execute(select(Portfolio).where(Portfolio.user_id == user_id))
        portfolios = result.scalars().all()
        holdings_data = []
        for p in portfolios:
            h_result = await db.execute(select(Holding).where(Holding.portfolio_id == p.id))
            for h in h_result.scalars().all():
                holdings_data.append({"portfolio": p.name, "symbol": h.symbol, "quantity": h.quantity, "avg_price": h.avg_price})
        messages = [
            SystemMessage(content="You are a portfolio optimizer. Analyze holdings and suggest rebalancing. Return JSON."),
            HumanMessage(content=f"Optimize this portfolio: {holdings_data}. Suggest allocation changes, risk adjustments, and diversification improvements."),
        ]
        result = await self.llm.ainvoke(messages)
        return {"recommendations": result.content, "agent": "portfolio_optimizer"}

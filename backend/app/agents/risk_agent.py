from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from ..core.config import settings


class RiskAgent:
    def __init__(self):
        if settings.llm_provider == "ollama":
            self.llm = ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.2)
        else:
            self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.2, api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def assess(self, symbol: str) -> dict:
        messages = [
            SystemMessage(content="You are a risk analyst. Assess investment risk. Return JSON."),
            HumanMessage(content=f"Assess risk for {symbol}. Include: VaR estimate, beta, volatility, Sharpe ratio estimate, max drawdown, risk score (1-10)."),
        ]
        result = await self.llm.ainvoke(messages)
        return {"symbol": symbol, "risk_assessment": result.content, "agent": "risk_agent"}

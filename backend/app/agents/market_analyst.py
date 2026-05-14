from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from ..core.config import settings


class MarketAnalystAgent:
    def __init__(self):
        if settings.llm_provider == "ollama":
            self.llm = ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.2)
        else:
            self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.2, api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def analyze(self, symbol: str) -> dict:
        messages = [
            SystemMessage(content="You are a market analyst. Provide technical and fundamental analysis. Return JSON."),
            HumanMessage(content=f"Analyze {symbol} stock. Include: trend, support/resistance, RSI, MACD, moving averages, fundamental metrics, recommendation. Be concise."),
        ]
        result = await self.llm.ainvoke(messages)
        return {"symbol": symbol, "analysis": result.content, "agent": "market_analyst"}

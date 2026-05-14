from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama
from langchain.schema import HumanMessage, SystemMessage
from ..core.config import settings


class SentimentAnalystAgent:
    def __init__(self):
        if settings.llm_provider == "ollama":
            self.llm = ChatOllama(base_url=settings.ollama_base_url, model=settings.llm_model, temperature=0.2)
        else:
            self.llm = ChatOpenAI(model=settings.llm_model, temperature=0.2, api_key=settings.openai_api_key, base_url=settings.openai_base_url)

    async def analyze(self, symbol: str) -> dict:
        messages = [
            SystemMessage(content="You are a sentiment analyst. Analyze market sentiment for stocks. Return JSON."),
            HumanMessage(content=f"Analyze sentiment for {symbol}. Consider: news sentiment, social media buzz, fear/greed, institutional activity. Score from -1 to 1."),
        ]
        result = await self.llm.ainvoke(messages)
        return {"symbol": symbol, "sentiment": result.content, "agent": "sentiment_analyst"}

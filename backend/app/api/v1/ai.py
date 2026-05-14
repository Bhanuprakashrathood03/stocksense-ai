from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from ...core.database import get_db
from ...core.redis import cache_get, cache_set
from ...api.deps import get_current_user
from ...models.user import User
from ...models.chat import ChatHistory, AIReport
from ...schemas.ai import ChatRequest, ChatResponse, InsightRequest
from ...agents.market_analyst import MarketAnalystAgent
from ...agents.sentiment_analyst import SentimentAnalystAgent
from ...agents.portfolio_optimizer import PortfolioOptimizerAgent
from ...agents.risk_agent import RiskAgent
from ...agents.report_generator import ReportGenerator
from ...services.ai_service import AIService

router = APIRouter()


@router.post("/chat")
async def chat(req: ChatRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    ai_service = AIService(user, db)
    response, session_id = await ai_service.chat(req.message, req.session_id)
    return ChatResponse(response=response, session_id=session_id)


@router.get("/history")
async def get_chat_history(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ChatHistory).where(ChatHistory.user_id == user.id).order_by(desc(ChatHistory.created_at)).limit(50)
    )
    messages = result.scalars().all()
    return [{"role": m.role, "content": m.content, "session_id": m.session_id, "created_at": m.created_at} for m in messages]


@router.get("/insights/{symbol}")
async def get_insights(symbol: str, user: User = Depends(get_current_user)):
    cached = await cache_get(f"insight:{symbol}")
    if cached:
        return cached
    agent = MarketAnalystAgent()
    result = await agent.analyze(symbol.upper())
    await cache_set(f"insight:{symbol}", result, 600)
    return result


@router.get("/reports")
async def get_reports(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(AIReport).where(AIReport.user_id == user.id).order_by(desc(AIReport.created_at)).limit(20)
    )
    reports = result.scalars().all()
    return [{"id": r.id, "type": r.type, "title": r.title, "created_at": r.created_at} for r in reports]


@router.post("/analyze/{symbol}")
async def analyze_symbol(symbol: str, user: User = Depends(get_current_user)):
    agent = MarketAnalystAgent()
    sentiment = SentimentAnalystAgent()
    risk = RiskAgent()
    market = await agent.analyze(symbol.upper())
    sent = await sentiment.analyze(symbol.upper())
    risk_data = await risk.assess(symbol.upper())
    return {"market_analysis": market, "sentiment": sent, "risk": risk_data}


@router.post("/optimize-portfolio")
async def optimize_portfolio(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    optimizer = PortfolioOptimizerAgent()
    result = await optimizer.optimize(user.id, db)
    return result


@router.post("/generate-report")
async def generate_report(type: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    agent = ReportGenerator()
    report = await agent.generate(user.id, type, db)
    return report

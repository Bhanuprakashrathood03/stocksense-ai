from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...models.portfolio import Portfolio, Holding
from ...schemas.portfolio import PortfolioCreate, PortfolioResponse, HoldingCreate, HoldingResponse

router = APIRouter()


@router.get("")
async def list_portfolios(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Portfolio).where(Portfolio.user_id == user.id))
    portfolios = result.scalars().all()
    return [PortfolioResponse.model_validate(p) for p in portfolios]


@router.post("", status_code=201)
async def create_portfolio(req: PortfolioCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    portfolio = Portfolio(user_id=user.id, name=req.name, risk_profile=req.risk_profile, cash_balance=req.cash_balance)
    db.add(portfolio)
    await db.flush()
    return PortfolioResponse.model_validate(portfolio)


@router.get("/{portfolio_id}")
async def get_portfolio(portfolio_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user.id))
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(404, "Portfolio not found")
    return PortfolioResponse.model_validate(portfolio)


@router.post("/{portfolio_id}/holdings", status_code=201)
async def add_holding(portfolio_id: str, req: HoldingCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Portfolio).where(Portfolio.id == portfolio_id, Portfolio.user_id == user.id))
    portfolio = result.scalar_one_or_none()
    if not portfolio:
        raise HTTPException(404, "Portfolio not found")
    holding = Holding(portfolio_id=portfolio_id, symbol=req.symbol.upper(), quantity=req.quantity, avg_price=req.avg_price)
    db.add(holding)
    await db.flush()
    return HoldingResponse.model_validate(holding)


@router.delete("/{portfolio_id}/holdings/{holding_id}")
async def remove_holding(portfolio_id: str, holding_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Holding).where(Holding.id == holding_id, Holding.portfolio_id == portfolio_id))
    holding = result.scalar_one_or_none()
    if not holding:
        raise HTTPException(404, "Holding not found")
    await db.delete(holding)
    return {"ok": True}

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...models.portfolio import Portfolio, Holding
from ...models.stock import StockSignal

router = APIRouter()


@router.get("/overview")
async def overview(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Portfolio).where(Portfolio.user_id == user.id))
    portfolios = result.scalars().all()
    total_value = sum(p.total_value for p in portfolios)
    total_cash = sum(p.cash_balance for p in portfolios)
    count = len(portfolios)
    return {"portfolio_count": count, "total_value": total_value, "total_cash": total_cash, "invested": total_value - total_cash}


@router.get("/performance")
async def performance(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id)
    )
    portfolios = result.scalars().all()
    data = []
    for p in portfolios:
        data.append({"id": p.id, "name": p.name, "value": p.total_value, "cash": p.cash_balance})
    return data

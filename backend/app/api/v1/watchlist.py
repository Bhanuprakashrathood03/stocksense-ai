from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...models.portfolio import Watchlist
from ...schemas.portfolio import WatchlistResponse

router = APIRouter()


@router.get("")
async def get_watchlist(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Watchlist).where(Watchlist.user_id == user.id))
    items = result.scalars().all()
    return [WatchlistResponse.model_validate(w) for w in items]


@router.post("", status_code=201)
async def add_to_watchlist(symbol: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Watchlist).where(Watchlist.user_id == user.id, Watchlist.symbol == symbol.upper())
    )
    if result.scalar_one_or_none():
        raise HTTPException(400, "Already in watchlist")
    wl = Watchlist(user_id=user.id, symbol=symbol.upper())
    db.add(wl)
    await db.flush()
    return WatchlistResponse.model_validate(wl)


@router.delete("/{symbol}")
async def remove_from_watchlist(symbol: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Watchlist).where(Watchlist.user_id == user.id, Watchlist.symbol == symbol.upper())
    )
    wl = result.scalar_one_or_none()
    if not wl:
        raise HTTPException(404, "Not in watchlist")
    await db.delete(wl)
    return {"ok": True}

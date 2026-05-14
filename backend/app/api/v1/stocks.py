from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
import httpx

from ...core.database import get_db
from ...core.config import settings
from ...core.redis import cache_get, cache_set
from ...api.deps import get_current_user
from ...models.user import User
from ...models.stock import StockSignal
from ...schemas.stock import StockSearchResult, StockQuote, StockHistory, SignalResponse

router = APIRouter()

FINNHUB_BASE = "https://finnhub.io/api/v1"


async def finnhub_get(path: str, params: dict = None):
    if params is None:
        params = {}
    params["token"] = settings.finnhub_api_key
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{FINNHUB_BASE}{path}", params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()


@router.get("/search")
async def search_stocks(q: str):
    cached = await cache_get(f"search:{q}")
    if cached:
        return cached
    data = await finnhub_get("/search", {"q": q})
    results = [StockSearchResult(**r) for r in data.get("result", [])]
    await cache_set(f"search:{q}", [r.model_dump() for r in results], 60)
    return results


@router.get("/{symbol}")
async def get_stock(symbol: str):
    cached = await cache_get(f"quote:{symbol}")
    if cached:
        return cached
    quote = await finnhub_get("/quote", {"symbol": symbol.upper()})
    profile = await finnhub_get("/stock/profile2", {"symbol": symbol.upper()})
    result = {
        "symbol": symbol.upper(),
        "price": quote.get("c", 0),
        "change": quote.get("d", 0),
        "change_pct": quote.get("dp", 0),
        "volume": quote.get("v", 0),
        "high_52w": profile.get("52WeekHigh"),
        "low_52w": profile.get("52WeekLow"),
        "name": profile.get("name", ""),
        "exchange": profile.get("exchange", ""),
    }
    await cache_set(f"quote:{symbol}", result, 30)
    return result


@router.get("/{symbol}/history")
async def get_history(symbol: str, resolution: str = "D"):
    cached = await cache_get(f"history:{symbol}:{resolution}")
    if cached:
        return cached
    import time
    now = int(time.time())
    year_ago = now - 365 * 86400
    data = await finnhub_get("/stock/candle", {"symbol": symbol.upper(), "resolution": resolution, "from": year_ago, "to": now})
    if data.get("s") != "ok":
        raise HTTPException(400, "No data")
    candles = []
    for i in range(len(data["t"])):
        candles.append({
            "date": data["t"][i],
            "open": data["o"][i],
            "high": data["h"][i],
            "low": data["l"][i],
            "close": data["c"][i],
            "volume": data["v"][i],
        })
    await cache_set(f"history:{symbol}:{resolution}", candles, 300)
    return candles


@router.get("/{symbol}/signals")
async def get_signals(symbol: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(StockSignal).where(StockSignal.symbol == symbol.upper()).order_by(desc(StockSignal.created_at)).limit(20)
    )
    signals = result.scalars().all()
    return [SignalResponse.model_validate(s) for s in signals]

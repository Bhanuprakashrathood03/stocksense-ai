from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...models.subscription import Subscription, SubscriptionStatus
from ...schemas.subscription import SubscriptionResponse, UpgradeRequest

router = APIRouter()

PLANS = {"free": 0, "pro": 1, "enterprise": 2}


@router.get("")
async def get_subscription(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(404, "No subscription found")
    return SubscriptionResponse.model_validate(sub)


@router.post("/upgrade")
async def upgrade(req: UpgradeRequest, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if req.plan not in PLANS:
        raise HTTPException(400, "Invalid plan")
    result = await db.execute(select(Subscription).where(Subscription.user_id == user.id))
    sub = result.scalar_one_or_none()
    if not sub:
        sub = Subscription(user_id=user.id, plan=req.plan)
        db.add(sub)
    else:
        sub.plan = req.plan
        sub.status = SubscriptionStatus.active
    user.plan = req.plan
    await db.flush()
    return SubscriptionResponse.model_validate(sub)

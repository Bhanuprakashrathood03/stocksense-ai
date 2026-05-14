from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...models.alert import Alert, AlertCondition
from ...schemas.alert import AlertCreate, AlertResponse

router = APIRouter()


@router.get("")
async def list_alerts(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.user_id == user.id).order_by(desc(Alert.created_at)))
    return [AlertResponse.model_validate(a) for a in result.scalars().all()]


@router.post("", status_code=201)
async def create_alert(req: AlertCreate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    try:
        condition = AlertCondition(req.condition)
    except ValueError:
        raise HTTPException(400, f"Invalid condition: {req.condition}")
    alert = Alert(user_id=user.id, symbol=req.symbol.upper(), condition=condition, threshold=req.threshold)
    db.add(alert)
    await db.flush()
    return AlertResponse.model_validate(alert)


@router.patch("/{alert_id}/toggle")
async def toggle_alert(alert_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.user_id == user.id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(404, "Alert not found")
    alert.active = not alert.active
    await db.flush()
    return AlertResponse.model_validate(alert)


@router.delete("/{alert_id}")
async def delete_alert(alert_id: str, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Alert).where(Alert.id == alert_id, Alert.user_id == user.id))
    alert = result.scalar_one_or_none()
    if not alert:
        raise HTTPException(404, "Alert not found")
    await db.delete(alert)
    return {"ok": True}

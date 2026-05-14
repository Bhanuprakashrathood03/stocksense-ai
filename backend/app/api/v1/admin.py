from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from ...core.database import get_db
from ...api.deps import get_admin_user
from ...models.user import User

router = APIRouter()


@router.get("/users")
async def admin_list_users(admin: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).order_by(User.created_at.desc()).limit(100))
    users = result.scalars().all()
    return [
        {"id": u.id, "email": u.email, "name": u.name, "role": u.role.value, "plan": u.plan.value, "is_active": u.is_active, "created_at": u.created_at}
        for u in users
    ]


@router.get("/stats")
async def admin_stats(admin: User = Depends(get_admin_user), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(func.count(User.id)))
    total_users = result.scalar()
    result = await db.execute(select(func.count(User.id)).where(User.is_active == True))
    active_users = result.scalar()
    return {"total_users": total_users, "active_users": active_users}

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ...core.database import get_db
from ...api.deps import get_current_user
from ...models.user import User
from ...schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return UserResponse.model_validate(user)


@router.patch("/me")
async def update_me(req: UserUpdate, user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    if req.name is not None:
        user.name = req.name
    if req.email is not None:
        user.email = req.email
    db.add(user)
    await db.commit()
    return UserResponse.model_validate(user)

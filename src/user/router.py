from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.user import models
from src.database import get_db
from src.auth import schemas

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.get('/{id}', response_model=schemas.UserOut)
async def get_user(id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.User).filter(models.User.id == id)
    user = await db.execute(query)
    user = user.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")

    return user

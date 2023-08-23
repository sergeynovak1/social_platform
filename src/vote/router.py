from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src import database
from src.auth import oauth2
from src.vote import schemas, models


router = APIRouter(
    prefix="/vote",
    tags=['Vote']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: AsyncSession = Depends(database.get_db), current_user: int = Depends(
    oauth2.get_current_user)):
    vote_query = await db.execute(select(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                                              models.Vote.user_id == current_user.id))
    found_vote = vote_query.scalar_one_or_none()

    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        await db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        await db.delete(found_vote)
        await db.commit()
        return {"message": "successfully deleted vote"}

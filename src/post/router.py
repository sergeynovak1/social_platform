from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List

from src.auth import oauth2
from src.database import get_db
from src.post import schemas, models as post_models
from src.vote import models as vote_models

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


# @router.get("/", response_model=List[schemas.PostOut])
# async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
#               limit: int = 10, skip: int = 0, search: str = ""):
#     posts = db.query(post_models.Post, func.count(vote_models.Vote.post_id).label("votes")).join(
#         vote_models.Vote, vote_models.Vote.post_id == post_models.Post.id, isouter=True).group_by(
#         post_models.Post.id).filter(
#         post_models.Post.title.contains(search)).limit(limit).offset(skip).all()
#     return posts


@router.get("/")
async def get_posts(db: AsyncSession = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    limit: int = 10, skip: int = 0, search: str = ""):
    query = select(
        post_models.Post
    ).filter(
        post_models.Post.title.contains(search)
    ).limit(limit).offset(skip)

    result = await db.execute(query)

    posts_with_votes = result.scalars().all()

    post_objects = [
        schemas.PostExample(
            **{**post.__dict__}
        )
        for post in posts_with_votes
    ]
    return post_objects


# @router.get("/my-posts", response_model=List[schemas.Post])
# def my_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     posts = db.query(post_models.Post).filter(post_models.Post.owner_id == current_user.id).all()
#     return posts


@router.post("/create-post", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
async def create_post(post: schemas.PostCreate, db: AsyncSession = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    new_post = post_models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    await db.commit()
    await db.refresh(new_post)

    return new_post


# @router.get("/{id}", response_model=schemas.PostOut)
# def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#     post = db.query(post_models.Post, func.count(vote_models.Vote.post_id).label("votes")).join(
#         vote_models.Vote, vote_models.Vote.post_id == post_models.Post.id, isouter=True).group_by(post_models.Post.id).filter(
#         post_models.Post.id == id).first()
#
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"post with id: {id} was not found")
#     return post


@router.get("/{id}", response_model=schemas.PostExample)
async def get_post(id: int, db: AsyncSession = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = await db.execute(select(post_models.Post).where(post_models.Post.id == id))
    post = post_query.scalars().first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: AsyncSession = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = await db.execute(select(post_models.Post).where(post_models.Post.id == id))
    post = post_query.scalars().first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    await db.delete(post)

    await db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, updated_post: schemas.PostCreate, db: AsyncSession = Depends(get_db),
                      current_user: int = Depends(oauth2.get_current_user)):
    post_query = await db.execute(select(post_models.Post).where(post_models.Post.id == id))
    post = post_query.scalars().first()

    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    await db.execute(
        update(post_models.Post).where(post_models.Post.id == id).values(**updated_post.dict())
    )
    await db.commit()

    return post

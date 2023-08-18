from fastapi import FastAPI, Response, status, HTTPException, Depends

from src.post import router as post
from src.vote import router as vote
from src.auth import router as auth
from src.user import router as user

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

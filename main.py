from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


@app.get('/')
async def root():
    return {'message': 'Hello world'}


@app.get('/posts')
def get_posts():
    return {'data': 'There are your posts'}


@app.post('/create-post')
def create_post(post: Post):
    print(post.model_dump())
    return{'data': post}

from fastapi import FastAPI
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


my_posts = [
    {'title': 'title1', 'content': 'content1', 'id': 1},
    {'title': 'title2', 'content': 'content2', 'id': 2}
]


@app.get('/')
async def root():
    return {'message': 'Hello world'}


@app.get('/posts')
def get_posts():
    return {'data': my_posts}


@app.post('/create-post')
def create_post(post: Post):
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)
    return{'data': post_dict}

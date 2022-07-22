
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 
my_posts = [{'title':'title of post1', 'content':'content of post1','id':1},
            {'title':'title of post2', 'content':'content of post2','id':2},]


def find_post(id):
    for p in my_posts:
        if(p['id'] == id):
            return p
        
def find_index_post(id):
    for i,p in enumarate(my_posts):
        if(p['id'] == id):
            return i
    

@app.get("/")
async def root():
    return {"message": "Welcome to My API!!!"}

@app.get('/posts')
def get_posts():
    return {'data': my_posts}

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    new_post = post.dict()
    new_post['id'] = max([int(post['id']) for post in my_posts]) +1
    my_posts.append(new_post)
    return { 'data': new_post }

@app.get('/posts/latest')
def get_latest_post():
    return my_posts[-1]

@app.get('/posts/{id}')
def get_post(id: int, response: Response):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'error': f"post with {id} was not found"}
    return {"post detail": post}

@app.delete('/posts/{id}')
def delete_post(id:int):
    index = find_index_post(id)
    my_posts.pop(index)
    return {'message': f'post with {id} was succesfully deleted'}


"""@app.put('/updateposts/{id}')
def update_posts(id: int, post : Post):
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == id:
            my_posts[i] = post.dict()
            return { 'data': post.dict() }
    return { 'data': 'Not Found' }"""
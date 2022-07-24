
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None
 
 
while True:
    try:
        conn = psycopg2.connect(host='localhost',database = 'fastapi',user='postgres',password='12345',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to Postgres")
        break
    except Exception as error:
        print('Cannection error:', error)
        time.sleep(2)
        







my_posts = [{'title':'title of post1', 'content':'content of post1','id':1},
            {'title':'title of post2', 'content':'content of post2','id':2},]


def find_post(id):
    for p in my_posts:
        if(p['id'] == id):
            return p
        
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if(p['id'] == id):
            return i
    

@app.get("/")
async def root():
    return {"message": "Welcome to My API!!!"}

@app.get('/posts')
def get_posts():
    get_all_sql = """SELECT * FROM posts;"""
    cursor.execute(get_all_sql)
    posts = cursor.fetchall()
    
    #return {'data': my_posts}
    return {'data': posts}
   

@app.post('/createposts', status_code=status.HTTP_201_CREATED)
def create_posts(post : Post):
    #new_post = post.dict()
    #new_post['id'] = max([int(post['id']) for post in my_posts]) +1
    #my_posts.append(new_post)
    #return { 'data': new_post }
    #insert_sql = f"INSERT INTO posts (title, content, published) VALUES ({post.title}, {post.content},{post.published})" There may be sql injection
    #this prevent sql injection
    insert_sql = """INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;"""
    cursor.execute(insert_sql,(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    
    return { 'data': new_post }

@app.get('/posts/latest')
def get_latest_post():
    return my_posts[-1]

@app.get('/posts/{id}')
def get_post(id: int):
    get_one_post_sql = """SELECT * FROM posts WHERE id = %s;"""
    cursor.execute(get_one_post_sql,(str(id),))
    post = cursor.fetchone()
    #post = find_post(id)
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'error': f"post with {id} was not found"}
    return {"post detail": post}

@app.delete('/posts/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    delete_sql = """DELETE FROM posts WHERE id = %s RETURNING *;"""
    cursor.execute(delete_sql,(str(id),))    
    deleted_post = cursor.fetchone()
    conn.commit()
    #index = find_index_post(id)
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    
    #my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put('/posts/{id}')
def update_post(id:int, post:Post):
    update_sql = """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""" 
    cursor.execute(update_sql,(post.title, post.content, post.published,str(id))) 
    updated_post = cursor.fetchone()
    conn.commit()

    #index = find_index_post(id)
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    
    #post_dict = post.dict()
    #post_dict['id'] = id
    #my_posts[index] = post_dict
    return {"data": updated_post}


"""@app.put('/updateposts/{id}')
def update_posts(id: int, post : Post):
    for i in range(len(my_posts)):
        if my_posts[i]['id'] == id:
            my_posts[i] = post.dict()
            return { 'data': post.dict() }
    return { 'data': 'Not Found' }"""
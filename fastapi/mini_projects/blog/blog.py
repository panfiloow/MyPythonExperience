from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime
import uvicorn

app = FastAPI(title="Blog API", version="1.0.0")

class CreatePost(BaseModel):
    title : str
    content : str
    published: bool = True


class Post(CreatePost):
    id : int
    created_at : datetime
    last_update : datetime | None = None

def get_next_id(post_db):
    if not post_db:
        return 1
    return max([post.id for post in post_db]) + 1
    

post_db : List[Post] = [
    Post(id=1, title="Пост1", content="Очень важный пост1", created_at=datetime.now()),
    Post(id=2, title="Пост2", content="Очень важный пост2", created_at=datetime.now()), 
    Post(id=3, title="Пост3", content="Очень важный пост3", created_at=datetime.now()),  
]

@app.get("/")
async def root():
    return {"status": "server work"}

@app.get("/posts")
async def get_posts(skip : int = 0, limit: int = 100) -> List[Post]:
    return post_db[skip:limit+skip]

@app.get("/posts/{post_id}")
async def get_post_by_id(post_id: int):
    for post in post_db:
        if post.id == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден")

@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: CreatePost):
    new_post = Post(id=get_next_id(post_db), created_at=datetime.now(), **post.model_dump())
    post_db.append(new_post)
    return {"msg": "Пост успешно создан"}

@app.put("/posts/{post_id}")
async def change_post(post_id: int, update: CreatePost):
    for index, post in enumerate(post_db):
        if post.id == post_id:
            updated_post = post.copy(update=update.dict())
            updated_post.last_update = datetime.now()
            post_db[index] = updated_post
            return {"msg": "Пост изменен", "post": updated_post}

@app.delete("/posts/{post_id}")
async def delete_post(post_id : int):
    for post in post_db:
        if post.id == post_id:
            post_db.remove(post)
            return {"msg": "Пост успешно удален"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Пост не найден")
   

if __name__ == "__main__":
    uvicorn.run("blog:app", host="127.0.0.1", port=8000, reload=True)

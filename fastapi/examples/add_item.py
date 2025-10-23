from typing import Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 1. Определите Pydantic-модель Item с полями: id (int), name (str), description (str, необязательный), price (float), tax (float, необязательный).

class Item(BaseModel):
    id : int
    name : str
    description : Optional[str] = None
    price : float
    tax : Optional[float] = None


#2. Создайте "базу данных" в виде списка словарей или объектов Item.
items_db = [ 
    Item(id=1, name="Item1", description="Desc Item1", price=100),
    Item(id=2, name="Item2", description="Desc Item2", price=100.56, tax=10),
    Item(id=3, name="Item3", description="Desc Item3", price=150.56, tax=10.21)
]


@app.get("/")
async def root():
    return {"msg": "server working"}

@app.get("/items")
async def get_items() -> list[Item]:
    return items_db

@app.get("/items/{item_id}")
async def get_item_by_id(item_id : int) -> Item:
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

#3.  Создайте эндпоинт POST /items/, который принимает объект Item в теле запроса (объявите параметр функции как item: Item). 
#    Функция должна добавлять новый item в вашу "базу данных" и возвращать его.

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
async def add_item(item: Item) -> Item:
    if any(existing_item.id == item.id for existing_item in items_db):
        raise HTTPException(status_code=400, detail="Item with this ID already exists")
    
    items_db.append(item)
    return item
    

#4. Создайте эндпоинт DELETE /items/{item_id}. 
#   При успешном удалении возвращайте статус 200 OK (или 204 No Content).
#   Если item для удаления не найден, возвращайте 404 Not Found.

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id : int):
    for item in items_db:
        if item_id == item.id:
            items_db.remove(item)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

if __name__ == "__main__":
    uvicorn.run("add_item:app", host="127.0.0.1", port=8000, reload=True)
from typing import List, Optional
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# 1. Определите Pydantic-модель Item с полями: id (int), name (str), description (str, необязательный), price (float), tax (float, необязательный).


class UpdateItem(BaseModel):
    name : Optional[str] = None
    description : Optional[str] = None
    price : Optional[float] = None
    tax : Optional[float] = None

class CreateItem(BaseModel):
    name : str
    description : Optional[str] = None
    price : float
    tax : Optional[float] = None

class Item(CreateItem):
    id : int

def generate_next_id(items_db : List[Item]) -> int:
    return max([item.id for item in items_db]) + 1



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
async def add_item(item: CreateItem) -> Item:
    nex_item = Item(id=generate_next_id(items_db), **item.model_dump())
    items_db.append(nex_item)
    return nex_item
    

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


# 5. Создайте эндпоинт PUT /items/{item_id}. 
#   Он должен принимать модель Item и полностью заменять старый item на новый (по item_id).
#   Не забудьте про обработку ошибки 404.

@app.put("/items/{item_id}", status_code=status.HTTP_200_OK)
async def change_item(item_id : int, item: CreateItem):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updated_item = Item(id=item_id, **item.model_dump())
            items_db[index] = updated_item
            return {"msg": "Объект успешно изменен"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")


# 6. Создайте эндпоинт PATCH /items/{item_id}. 
# Он должен принимать не всю модель Item, а другую Pydantic-модель, например ItemUpdate, где все поля необязательные. 
# Внутри функции:
# Найдите существующий item.
# Получите данные для обновления в виде словаря (exclude_unset=True).
# Обновите только те поля, которые пришли в запросе.
# Сохраните изменения.
@app.patch("/items/{item_id}", status_code=status.HTTP_200_OK)
async def update_item(item_id : int, update_item : UpdateItem):
    for index, existing_item in enumerate(items_db):
        if existing_item.id == item_id:
            updates = update_item.model_dump(exclude_unset=True, exclude_none=True)
            if not updates:
                return{"msg": "Укажите, что нужно изменить"}
            updated_item = existing_item.model_copy(update=updates)
            items_db[index] = updated_item
            return {"msg": "Объект успешно обновлен"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item not found")

if __name__ == "__main__":
    uvicorn.run("items:app", host="127.0.0.1", port=8000, reload=True)
    
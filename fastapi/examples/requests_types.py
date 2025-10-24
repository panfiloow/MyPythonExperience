# HTTP Методы (HTTP Verbs) в REST API
# Каждый метод имеет семантическое значение и определяет тип операции над ресурсом.

# 1. GET - Получение данных
# Назначение: Чтение или получение данных с сервера.

# Характеристики:

# Безопасный (не изменяет состояние сервера)

# Идемпотентный (многократный вызов дает одинаковый результат)

# Кэшируемый


from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str

# Простой GET запрос
@app.get("/users/")
async def get_users():
    return {"message": "Список всех пользователей"}

# GET с параметром пути
@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}

# GET с query параметрами
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10, search: str = None):
    return {"skip": skip, "limit": limit, "search": search}


# 2. POST - Создание новых данных
# Назначение: Создание нового ресурса.

# Характеристики:

# Не безопасный (изменяет состояние)

# Не идемпотентный (каждый вызов создает новый ресурс)

users_db = []

@app.post("/users/")
async def create_user(user: User):
    users_db.append(user)
    return {"message": "Пользователь создан", "user": user}

# POST для сложных операций
@app.post("/users/{user_id}/activate")
async def activate_user(user_id: int):
    return {"message": f"Пользователь {user_id} активирован"}


# 3. PUT - Полное обновление
# Назначение: Полная замена ресурса.

# Характеристики:

# Клиент должен отправить ВСЕ поля

# Если ресурс не существует, может создавать новый (зависит от реализации)

# Идемпотентный

@app.put("/users/{user_id}")
async def update_user(user_id: int, user: User):
    # Ищем пользователя
    for idx, existing_user in enumerate(users_db):
        if existing_user.id == user_id:
            users_db[idx] = user  # Полная замена
            return {"message": "Пользователь полностью обновлен", "user": user}
    
    # Если не найден - создаем нового
    users_db.append(user)
    return {"message": "Пользователь создан", "user": user}


# 4. PATCH - Частичное обновление
# Назначение: Частичное обновление ресурса.

# Характеристики:

# Клиент отправляет только изменяемые поля

# Более эффективен для больших объектов

# Идемпотентный

# Способ 1: Использование Pydantic с exclude_unset=True
class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


@app.patch("/users/{user_id}")
async def partial_update_user(user_id: int, user_update: UserUpdate):
    # Находим пользователя
    for existing_user in users_db:
        if existing_user.id == user_id:
            # Получаем только переданные поля
            update_data = user_update.model_dump(exclude_unset=True)
            
            # Обновляем только переданные поля
            updated_user = existing_user.model_copy(update=update_data)
            
            # Сохраняем обновленного пользователя
            users_db[users_db.index(existing_user)] = updated_user
            
            return {"message": "Пользователь частично обновлен", "user": updated_user}
    
    return {"error": "Пользователь не найден"}

# Способ 2: Ручное обновление
@app.patch("/users/{user_id}")
async def patch_user(user_id: int, user_update: UserUpdate):
    for existing_user in users_db:
        if existing_user.id == user_id:
            # Обновляем только переданные поля
            if user_update.name is not None:
                existing_user.name = user_update.name
            if user_update.email is not None:
                existing_user.email = user_update.email
            
            return {"message": "Пользователь обновлен", "user": existing_user}
        

# 5. DELETE - Удаление данных
# Назначение: Удаление ресурса.

# Характеристики:

# Не безопасный

# Идемпотентный

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for user in users_db:
        if user.id == user_id:
            users_db.remove(user)
            return {"message": f"Пользователь {user_id} удален"}
    
    return {"error": "Пользователь не найден"}

# 6. Дополнительные методы
# HEAD - Получение заголовков
# Аналогичен GET, но без тела ответа.

# OPTIONS - Информация о поддерживаемых методах
# Что такое HTTP-статус код?
# HTTP-статус код — это трехзначное число, которое сервер отправляет клиенту в ответ на его запрос. Он сообщает клиенту о результате обработки запроса.
# Коды делятся на пять групп:

# 1xx (Информационные): Запрос принят, обработка продолжается.

# 2xx (Успех): Запрос был успешно получен, понят и обработан.

# 3xx (Перенаправление): Для завершения запроса требуются дальнейшие действия.

# 4xx (Ошибка клиента): Запрос содержит неправильный синтаксис или не может быть выполнен (например, неверные данные, нет доступа).

# 5xx (Ошибка сервера): Сервер не смог выполнить допустимый запрос из-за своей ошибки.

# Использование status_code в декораторах FastAPI
# В FastAPI самый простой и распространенный способ указать статус-код для успешного ответа 
# — это использовать параметр status_code в декораторе операции пути (@app.get, @app.post и т.д.).

# FastAPI предоставляет удобный список предопределенных констант в fastapi.status, чтобы вам не нужно было запоминать цифры.


# Пример 1: Создание ресурса (201 Created)

# Стандартная практика — возвращать статус 201 Created после успешного создания нового ресурса (например, нового элемента в БД).

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import HTTPBearer
from pydantic import BaseModel

# Создаем модель Pydantic для данных Item
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()

# Используем status_code=201 для успешного создания
@app.post("/items/", status_code=status.HTTP_201_CREATED)
async def create_item(item: Item):
    # Здесь обычно логика сохранения item в базу данных
    # ...
    return item  # FastAPI автоматически вернет этот объект с статусом 201

# Что происходит:

# Клиент отправляет POST запрос на /items/ с данными в теле (JSON).

# Если данные валидны и обработка прошла успешно, ваша функция возвращает объект item.

# FastAPI берет этот объект, сериализует его в JSON и устанавливает HTTP-статус код ответа 201.

# Клиент видит статус 201 и понимает, что ресурс был создан.


# Пример 2: Стандартные успешные операции

app = FastAPI()

@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_items():
    # Логика получения списка items
    items = ["item1", "item2"]
    return items
# Для GET 200 OK является статусом по умолчанию, так что status_code можно не указывать.

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int):
    # Логика удаления item из базы данных
    # ...
    # Для 204 НЕЛЬЗЯ возвращать тело ответа. FastAPI это знает.
    return  # Просто возвращаем None

# Важные моменты:

# 204 No Content: Используется для успешных операций, которые не возвращают никакого тела (например, удаление). FastAPI не будет пытаться сериализовать возвращаемое значение в тело ответа.

# Значение по умолчанию: Для GET обычно 200, для POST — 200, но лучше явно указывать 201 для создания.



# Часть 2: Исключения и HTTPException
# Зачем нужно HTTPException?
# Параметр status_code в декораторе предназначен для успешных ответов. Но что, если произошла ошибка? 
# Например, клиент запросил несуществующий элемент, отправил невалидные данные или у него нет прав.

# Для таких ситуаций используется HTTPException.

# Что такое HTTPException?
# HTTPException — это специальный класс исключений в FastAPI, предназначенный именно для возврата ошибок клиенту. 
# Когда вы вызываете это исключение внутри своей функции (внутри эндпоинта или любой зависимой функции), 
# FastAPI перехватывает его, прерывает обычное выполнение кода и сразу отправляет клиенту HTTP-ответ с указанным статус-кодом и деталями.

# Общий вид
# HTTPException(status_code=код_ошибки, detail=сообщение_об_ошибке)

# Пример 1: Элемент не найден (404 Not Found)

# Самый классический пример.
app = FastAPI()

# "База данных" для примера
fake_items_db = {"plumbus": {"name": "Plumbus", "price": 10.99}}

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id not in fake_items_db:
        # Вызываем исключение, если элемент не найден
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Item not found"  # Простое строковое сообщение
        )
    return fake_items_db[item_id]

# Что происходит:

# Клиент запрашивает GET /items/unknown_id.
# Ваш код проверяет наличие item_id в "базе данных".
# Так как его там нет, выполняется raise HTTPException(...).
# FastAPI немедленно перехватывает это исключение, не выполняя код дальше (например, return fake_items_db[item_id]).
# Клиент получает ответ с статусом 404 и телом:
{
  "detail": "Item not found"
}

# Пример 2: Расширенные детали ошибки

# Часто клиенту нужно передать больше информации, чем просто строка. Вы можете передать в detail словарь или список.
app = FastAPI()

# Модель для расширенной ошибки
class ValidationErrorDetail(BaseModel):
    field: str
    error_type: str
    message: str

# @app.post("/complex-items/")
# async def create_complex_item(/* ... */):
#     # Допустим, произошла какая-то сложная ошибка валидации
#     # Вместо строки возвращаем структурированный объект
#     raise HTTPException(
#         status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
#         detail={
#             "error": "Validation Failed",
#             "messages": [
#                 {"field": "price", "error": "negative_value", "message": "Price must be positive"},
#                 {"field": "name", "error": "too_short", "message": "Name must be at least 3 characters"}
#             ]
#         }
#     )

# Пример 3: Ошибка доступа (403 Forbidden)
security = HTTPBearer()
app = FastAPI()

def get_current_user(token: str = Depends(security)):
    # Упрощенная логика проверки токена
    if token.credentials != "secret-token":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            # Иногда добавляют специальные заголовки (как в спецификации HTTP)
            headers={"WWW-Authenticate": "Bearer"},
        )
    return {"user": "admin"}

@app.get("/admin/")
async def admin_route(current_user: dict = Depends(get_current_user)):
    # Этот код выполнится, только если пользователь прошел аутентификацию
    return {"message": "Welcome to the admin panel!"}

# Ключевой момент: 
# HTTPException можно вызывать не только в самом эндпоинте, но и в зависимостях (Dependencies), 
# что делает его мощным инструментом для централизованной проверки прав доступа и валидации.


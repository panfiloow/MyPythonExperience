from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Book(BaseModel):
    id : int
    title: str
    author: str
    year : int
    is_available : bool

class BookCreate(BaseModel):
    title: str
    author: str
    year: int
    is_available: bool = True  

books_db = [
    Book(id=0, title="Преступление и наказание", author="Федор Достоевский", year=1866, is_available=True),
    Book(id=1, title="Мастер и Маргарита", author="Михаил Булгаков", year=1967, is_available=False),
    Book(id=2, title="1984", author="Джордж Оруэлл", year=1949, is_available=True)
]

def generate_next_book_id(books_db):
    if not books_db:
        return 0
    return max(book.id for book in books_db) + 1

def duplicate_check(books_db, book) -> bool:
    duplicate = [duplicate for duplicate in books_db if duplicate.title == book.title and duplicate.author == book.author and duplicate.year == book.year]
    if duplicate:
        return False
    return True
    
@app.get("/", tags=["Книги"], description="Приветствие")
async def greatings():
    return {"message": "Добро пожаловать в систему управления книгами"}

@app.get("/books", tags=["Книги"], description="Получить все книги")
async def get_books(available_only: bool | None = None, author: str | None = None):
    filtered_books = books_db
    
    if author:
        filtered_books = [book for book in filtered_books if book.author.lower() == author.lower()]
    
    if available_only:
        filtered_books = [book for book in filtered_books if book.is_available]
    
    return filtered_books

@app.get("/books/{book_id}", tags=["Книги"], description="Получить книгу по id")
async def get_book_by_id(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book  
    
    raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")

@app.post("/books", tags=["Книги"], description="Добавить книгу в базу данных")
async def add_book(book_data: BookCreate):  
    new_book = Book(
        id=generate_next_book_id(books_db),
        title=book_data.title,
        author=book_data.author,
        year=book_data.year,
        is_available=book_data.is_available
    )
    
    if not duplicate_check(books_db, new_book):
        raise HTTPException(status_code=409, detail="Книга уже есть в базе")
    
    books_db.append(new_book)
    return {"status_code": 200, "msg": "Книга успешно добавлена в базу", "book": new_book}

@app.put("/books/{book_id}", tags=["Книги"], description="Обновляет информацию о книге по id")
async def update_book_info_by_id(book_id: int, updated_book: Book):
    if updated_book.id != book_id:
        raise HTTPException(status_code=400, detail="ID в пути и в теле запроса не совпадают")
    
    for i, book in enumerate(books_db):
        if book.id == book_id:
            books_db[i] = updated_book
            return {"message": "Книга успешно обновлена", "book": updated_book}
    
    raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")

@app.delete("/books/{book_id}", tags=["Книги"], description="Удаляет книгу по id")
async def delete_book_by_id(book_id: int):
    for i, book in enumerate(books_db):
        if book.id == book_id:
            deleted_book = books_db.pop(i)
            return {"status_code": 200, "msg": f"Книга '{deleted_book.title}' удалена"}
    
    raise HTTPException(status_code=404, detail=f"Книга с ID {book_id} не найдена")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("book:app", host="127.0.0.1", port=8000, reload=True)

import datetime
from typing import List, Optional
"""

Уровень 1: Начальный
Задача 1.1: Класс "Студент"
Создайте класс Student с атрибутами:

name (имя)

age (возраст)

grades (список оценок)

Методы:

add_grade(grade) - добавить оценку

get_average() - вернуть средний балл

is_excellent() - вернуть True, если средний балл >= 4.5

# Пример использования:
student = Student("Alice", 20)
student.add_grade(5)
student.add_grade(4)
student.add_grade(5)
print(student.get_average())  # 4.67
print(student.is_excellent())  # True



Задача 1.2: Класс "Прямоугольник"
Создайте класс Rectangle с атрибутами width и height.
Реализуйте методы:

area() - площадь

perimeter() - периметр

is_square() - является ли квадратом

"""


class Student:
    
    def __init__(self, name : str, age : int, grades: list = None):
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Name must be a non-empty string")
        if not isinstance(age, int) or age <= 0:
            raise ValueError("Age must be a positive integer")
        
        self.name = name 
        self.age = age
        self.grades = grades if grades is not None else []
        
        for grade in self.grades:
            self._validate_grade(grade)
        
    def add_grade(self, grade):
        self._validate_grade(grade)
        self.grades.append(grade)
    
    def get_average(self):
        if not self.grades:
            return 0.0
        return round(sum(self.grades) / len(self.grades), 2)
    
    def is_excellent(self):
        return self.get_average() >= 4.5
    
    def _validate_grade(self, grade):
        if not isinstance(grade, (int, float)) or not (1 <= grade <= 5):
            raise ValueError(f"Grade must be a number between 1 and 5, got {grade}")
        
    def __str__(self):
        return f"Student(name='{self.name}', age={self.age}, average={self.get_average()})"

    def __repr__(self):
        return f"Student('{self.name}', {self.age}, {self.grades})"
    
""" 
проверка работы класса Student   
student = Student("Alice", 20)
student.add_grade(5)
student.add_grade(4)
student.add_grade(5)
print(student.get_average())  
print(student.is_excellent())  
student2 = Student("bob", 20)
print(student2.get_average())
print(str(student))
print(repr(student))
""" 
class Rectangle:
    
    def __init__(self, width, height):
        self._validate_dimensions(width, height)
        self.width = width
        self.height = height
        
    def _validate_dimensions(self, width: float, height: float):
        if not isinstance(width, (int, float)) or not isinstance(height, (int, float)):
            raise TypeError(f"Width and height must be numbers, got width: {type(width).__name__}, height: {type(height).__name__}")
        
        if width < 0 or height < 0:
            raise ValueError(f"Width and height must be non-negative, got width: {width}, height: {height}")
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)
    
    def is_square(self):
        return self.width == self.height
    
    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"
    
    def __repr__(self) -> str:
        return f"Rectangle({self.width}, {self.height})"

"""
проверка для класса Rectangle 
rect1 = Rectangle(5, 3)
rect2 = Rectangle(4, 4)      
print(f"rect1: {rect1}")
print(f"Area: {rect1.area()}")           # 15
print(f"Perimeter: {rect1.perimeter()}") # 16
print(f"Is square: {rect2.is_square()}") # False
print(str(rect1))
"""

"""
Уровень 2: Средний
Задача 2.1: Банковский счет с историей
Расширьте класс BankAccount:

Добавьте историю операций (deposit/withdraw)

Реализуйте метод get_transaction_history()

Добавьте возможность установить лимит на снятие

class BankAccount:
    def __init__(self, account_holder: str, initial_balance: float = 0):
        self.account_holder = account_holder
        self._balance = initial_balance
    
    def get_balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    def __str__(self) -> str:
        return f"BankAccount(holder='{self.account_holder}', balance=${self._balance:.2f})"

Задача 2.2: Система управления библиотекой
Создайте классы:

Book (книга с названием, автором, годом издания)

Library (библиотека с коллекцией книг)

Методы для Library:

add_book(book)

remove_book(title)

find_books_by_author(author)

get_all_books_sorted_by_year()

"""

# Дано в условии задачи
class BankAccount:
    def __init__(self, account_holder: str, initial_balance: float = 0):
        self.account_holder = account_holder
        self._balance = initial_balance
    
    def get_balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> bool:
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def withdraw(self, amount: float) -> bool:
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    def __str__(self) -> str:
        return f"BankAccount(holder='{self.account_holder}', balance=${self._balance:.2f})"

# мой класс
class BankAccountWithHistory(BankAccount):
    
    def __init__(self, account_holder: str, initial_balance: float = 0, withdrawal_limit: float = None):
        
        super().__init__(account_holder, initial_balance)
        self.transaction_history = []
        self.withdrawal_limit = withdrawal_limit

        if initial_balance > 0:
            self.transaction_history.append(f"Initial - Deposit: ${initial_balance:.2f}")

    def deposit(self, amount):
        success = super().deposit(amount)
        if success:
            self.transaction_history.append(f"DEPOSIT - Amount: ${amount:.2f}, New Balance: ${self._balance:.2f}")
        return success
    
    def withdraw(self, amount):
        
        if self.withdrawal_limit and amount > self.withdrawal_limit:
            self.transaction_history.append(f"WITHDRAW FAILED - Amount: ${amount:.2f} exceeds limit ${self.withdrawal_limit:.2f}")
            return False
        
        success = super().withdraw(amount)
        if success :
            self.transaction_history.append(f"WITHDRAW - AMOUNT: ${amount:.2f}, New Balance: ${self._balance:.2f}")
        else:
            self.transaction_history.append(f"WITHDRAW FAILED - Insufficient funds: ${amount:.2f}")
        return success
    
    def get_transaction_history(self) -> list:
        return self.transaction_history.copy()
    
    def set_withdrawal_limit(self, limit: float) -> None:
        if limit is not None and limit < 0:
            raise ValueError("Withdrawal limit cannot be negative")
        self.withdrawal_limit = limit
        self.transaction_history.append(f"LIMIT SET - Withdrawal limit: ${limit:.2f}" if limit else "LIMIT REMOVED")
        
"""
проверка класса BankAccountWithHistory
account = BankAccountWithHistory("John Doe", 1000, withdrawal_limit=500)
    
print("=== Начальное состояние ===")
print(account)

print("\n=== Выполняем операции ===")
account.deposit(200)
account.withdraw(300)
account.withdraw(600)

for i, transaction in enumerate(account.get_transaction_history(), 1):
    print(f"{i:2d}. {transaction}")
"""



class Book():
    
    def __init__(self, title: str, author: str, publication_year: int):
        self._validate_data(title, author, publication_year)
        self.title = title
        self.author = author
        self.publication_year = publication_year
    
    def _validate_data(self, title, author, publication_year):
        if not isinstance(title, str) or not title.strip():
            raise ValueError(f"Title must be a non-empty string, got: {title}")
        if not isinstance(author, str) or not author.strip():
            raise ValueError(f"Author must be a non-empty string, got: {author}")
        if not isinstance(publication_year, int):
            raise ValueError(f"Publication year must be an integer, got: {type(publication_year).__name__}")
        
        current_year = datetime.datetime.now().year
        if publication_year < 1000 or publication_year > current_year + 2:  # +2 для авансовых изданий
            raise ValueError(f"Publication year must be between 1000 and {current_year + 2}, got: {publication_year}")
        
    def __str__(self) -> str:
        return f'"{self.title}" by {self.author} ({self.publication_year})'
    
    def __repr__(self) -> str:
        return f"Book('{self.title}', '{self.author}', {self.publication_year})"


class Library: 
    
    def __init__(self, books: List[Book] = None):
        self.books = books.copy() if books else []
             
    def add_book(self, book)-> None:
        if not isinstance(book, Book):
            raise ValueError(f"Book must be an instance of Book class, got: {type(book).__name__}")
        
        if book in self.books:
            print(f"Book '{book.title}' already exists in the library")
            return
        
        self.books.append(book)
        print(f"Added: {book}")
        
        

        
    def remove_book(self, title) -> bool:
        initial_count = len(self.books)
        self.books = [book for book in self.books if book.title.lower() != title.lower()]
        removed = initial_count != len(self.books)
        
        if removed:
            print(f"Removed book: {title}")
        else:
            print(f"Book not found: {title}")
        
        return removed 
        
    def find_books_by_author(self, author):
        return [book for book in self.books if book.author.lower() == author.lower()]
    
    def get_all_books_sorted_by_year(self, reverse: bool = False):
        return sorted(self.books, key=lambda book: book.publication_year, reverse=reverse)
    
    def __len__(self) -> int:
        return len(self.books)
    
    def __str__(self) -> str:
        if not self.books:
            return "Library is empty"
        
        books_list = "\n".join(f"  {i+1}. {book}" for i, book in enumerate(self.books))
        return f"Library contains {len(self.books)} books:\n{books_list}"



book1 = Book("Война и мир", "Л.Н. Толстой", 1800)
book2 = Book("Преступление и наказание", "Достоевский", 1900)

my_lib = Library([book2, book1])
print(str(my_lib))
my_lib.add_book(Book("Война и мир", "Л. Н. Тонкий", 1700))
print(str(my_lib))
my_lib.remove_book("Война и мир")
print(str(my_lib))
        


"""
Уровень 3: Продвинутый
Задача 3.1: Иерархия сотрудников
Создайте иерархию классов:

Employee (базовый класс)

Manager (наследует от Employee, имеет подчиненных)

Developer (наследует от Employee, имеет список языков программирования)

Реализуйте:

Полиморфизм метода calculate_bonus()

Метод для Manager, который возвращает всех подчиненных

Статический метод для подсчета общего количества сотрудников

Задача 3.2: Система заказов с декораторами
Создайте систему управления заказами:

Класс Product с ценой и названием

Класс Order с методами применения скидок через декораторы

Реализуйте декораторы для различных типов скидок

class Order:
    def __init__(self):
        self.products = []
    
    @discount_10_percent
    @seasonal_discount
    def calculate_total(self):
        return sum(p.price for p in self.products) 
"""



"""
Уровень 4: Экспертный
Задача 4.1: Собственный контекстный менеджер
Создайте класс-контекстный менеджер Timer, который:

Замеряет время выполнения блока кода

Автоматически сохраняет результаты в файл

Может быть использован как декоратор

Задача 4.2: Система плагинов
Создайте базовый класс Plugin с абстрактными методами.
Реализуйте систему, которая автоматически находит и загружает все классы-наследники Plugin из указанной директории.
 
"""
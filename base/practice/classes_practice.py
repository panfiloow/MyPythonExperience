from datetime import datetime
from typing import List, Optional, Callable, Any
import time
import json
from pathlib import Path

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


""" 
Демонстрация работы классов Book и Library
book1 = Book("Война и мир", "Л.Н. Толстой", 1800)
book2 = Book("Преступление и наказание", "Достоевский", 1900)

my_lib = Library([book2, book1])
print(str(my_lib))
my_lib.add_book(Book("Война и мир", "Л. Н. Тонкий", 1700))
print(str(my_lib))
my_lib.remove_book("Война и мир")
print(str(my_lib))
"""      


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
class Employee:
    
    _count = 0
    
    def __init__(self, name : str, surname: str, salary: float | int):
        self._validate_employee_data(name, surname, salary) 
        self.name = name
        self.surname = surname
        self.salary = salary
        Employee._count += 1
        
    def _validate_employee_data(self, name, surname, salary):
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Name must be not empty string, got {name}, type: {type(name).__name__}")
        if not isinstance(surname, str) or not surname.strip():
            raise ValueError(f"Surname must be not empty string, got {surname}, type: {type(surname).__name__}")
        if not isinstance(salary, (float, int)) or salary < 0:
            raise ValueError(f"Salary must be positive number, got {salary}, type: {type(salary).__name__}")
        
    @staticmethod
    def count_employee() -> int:
        return Employee._count
               

class Manager(Employee):
    
    def __init__(self, name : str, surname : str, salary : float, subordinates : List[Employee] = None):
        super().__init__(name, surname, salary)
        self._validate_subordinates(subordinates)
        self.suburdinates = subordinates if subordinates else []
    
    def calculate_bonus(self) -> float:
        return self.salary * 0.15
    
    def get_suburdinates(self) -> List[Employee]:
        return self.suburdinates.copy()
    
    def _validate_subordinates(self, subordinates):
        if subordinates is not None:
            if not all(isinstance(sub, (Employee, Developer)) for sub in subordinates):
                raise ValueError("All subordinates must be Employee instances")
        return subordinates
    
        

class Developer(Employee):
    
    def __init__(self, name, surname, salary, programming_languages: List[str] = None):
        super().__init__(name, surname, salary)
        self.programming_languages = programming_languages if programming_languages else []
    
    def calculate_bonus(self) -> float:
        return self.salary * 0.10
    
    def _validate_programming_languages(self, programming_languages):
        if programming_languages is not None:
            if not all(isinstance(lang, str) and lang.strip() for lang in programming_languages):
                raise ValueError("programming_languages must be list not empty strings")
            
"""
employee1 = Employee("Владлов", "Фролен", 50000)
developer1 = Developer("Владлен", "Фролов", 150000, ["js", "html", 'typescript', 'python'])            
manager1 = Manager("Фровлад", "Ленлов", 260000.24, [employee1, developer1])
print(Employee._count)
"""
def discount_10_percent(func):
        
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result * 0.9
        
    return wrapper
    
def seasonal_discount(func):
        
    def wrapper(*args, **kwargs):
        current_month = datetime.now().month
        
        if 3 <= current_month <= 5:  # весна
            discount = 0.08
        elif 6 <= current_month <= 8:  # лето
            discount = 0.05
        elif 9 <= current_month <= 11:  # осень
            discount = 0.10
        else:  # зима
            discount = 0.15
            
        result = func(*args, **kwargs)
        return result * (1 - discount)
    
    return wrapper



class Product():
    
    def __init__(self, name: str, price : float | int):
        self._validate_product_data(name, price)
        self.name = name
        self.price = price
    
    def _validate_product_data(self, name, price) -> None: 
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Product title must be not empty string, got {name} type: {type(name).__name__}")
        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError(f"Product price must be positive number, got {price} type:{type(price).__name__}")

class Order():
    
    def __init__(self, products : List[Product] = None):
        self._validate_products(products)
        self.products = products if products else []
    
    def _validate_products(self, products) -> None:
        if products is not None:
            if not all(isinstance(product, Product) for product in products):
                raise ValueError("All values in products must be Product class object")
    
    def add_products(self, products : List[Product]) -> None:
        self._validate_products(products)
        self.products.extend(products)
    
    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise ValueError("Product must be an instance of Product class")
        self.products.append(product)
    
    @discount_10_percent
    @seasonal_discount
    def calculate_total(self) -> float:
        if not self.products:
            return 0.0
        return sum(p.price for p in self.products) 
    
    def __str__(self) -> str:
        if not self.products:
            return "Заказ пуст"
        
        result = ["ЗАКАЗ"]
        result.append("=" * 50)
        
        for i, product in enumerate(self.products, 1):
            product_info = f"{i}. {product.name}" 
            product_info += f" - {product.price:.2f} ₽"
            result.append(product_info)
        
        result.append("=" * 50)
        result.append(f"Количество товаров: {len(self.products)}")
        
        base_total = sum(p.price for p in self.products)
        final_total = self.calculate_total()
        total_discount = base_total - final_total
        
        result.append(f"Сумма без скидок: {base_total:.2f} ₽")
        
        if total_discount > 0:
            discount_percent = (total_discount / base_total * 100)
            result.append(f"Общая скидка: -{total_discount:.2f} ₽ ({discount_percent:.1f}%)")
            result.append("-" * 30)
            result.append(f"ИТОГОВАЯ СУММА: {final_total:.2f} ₽")
        else:
            result.append(f"ИТОГОВАЯ СУММА: {final_total:.2f} ₽")
        
        return "\n".join(result)

"""      
product1 = Product("Банка Бандюэля", 100)
product2 = Product("Палмито", 300.55)
order1 = Order([product1])
print(str(order1))
order1.add_products([product2])
print(str(order1))
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

"""
Задача 4.1 без сохранения результатов в файл
class Timer():
    
    def __enter__(self):
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.exit_time = time.perf_counter()
        self.elapsed_time = self.exit_time - self.start_time
        print(f"Время выполнения: {self.elapsed_time:.6f} секунд")
        
    def __call__(self, func):
        
        def wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            exit_time = time.perf_counter()
            elapsed_time = exit_time - start_time
            print(f"Время выполнения: {elapsed_time:.6f} секунд")
            return result
        return wrapper

@Timer()
def test_timer_func():
    for i in range(101):
        if i > 99:
            print("Почти...")

with Timer() as timer:
    for i in range(101):
        if i > 99:
            print("Почти...")

test_timer_func()

""" 


class Timer:
    def __init__(
        self, 
        name: Optional[str] = None,
        log_file: str = "base/practice/timer_logs.json",
        unit: str = "seconds",
        verbose: bool = True
    ):
        self.name = name
        self.log_file = Path(log_file)
        self.unit = unit
        self.verbose = verbose
        self._ensure_log_file()
    
    def _ensure_log_file(self) -> None:
        if not self.log_file.exists():
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def _convert_time(self, seconds: float) -> float:
        units = {
            "seconds": 1,
            "milliseconds": 1000,
            "microseconds": 1000000,
            "minutes": 1/60
        }
        return seconds * units.get(self.unit, 1)
    
    def _get_unit_symbol(self) -> str:
        symbols = {
            "seconds": "s",
            "milliseconds": "ms",
            "microseconds": "μs",
            "minutes": "min"
        }
        return symbols.get(self.unit, "s")
    
    def _save_to_file(self, operation: str, elapsed: float) -> None:
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "name": self.name or operation,
                "elapsed_time": elapsed,
                "unit": self.unit,
                "operation": operation
            }
            
            logs.append(log_entry)
            
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(logs, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            print(f"Ошибка при сохранении в файл: {e}")
    
    def _format_time(self, elapsed_seconds: float) -> str:
        converted_time = self._convert_time(elapsed_seconds)
        symbol = self._get_unit_symbol()
        return f"{converted_time:.6f} {symbol}"
    
    def __enter__(self) -> 'Timer':
        self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.end_time = time.perf_counter()
        self.elapsed_time = self.end_time - self.start_time
        
        operation_name = self.name or "context_block"
        
        self._save_to_file(operation_name, self.elapsed_time)
        
        if self.verbose:
            formatted_time = self._format_time(self.elapsed_time)
            status = "с ошибкой" if exc_type else "успешно"
            print(f"[Timer] {operation_name} завершен {status}. Время: {formatted_time}")
    
    def __call__(self, func: Callable) -> Callable:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start_time = time.perf_counter()
            
            try:
                result = func(*args, **kwargs)
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                
                operation_name = self.name or func.__name__
                self._save_to_file(operation_name, elapsed_time)
                
                if self.verbose:
                    formatted_time = self._format_time(elapsed_time)
                    print(f"[Timer] {operation_name} завершен успешно. Время: {formatted_time}")
                
                return result
                
            except Exception as e:
                end_time = time.perf_counter()
                elapsed_time = end_time - start_time
                
                operation_name = self.name or func.__name__
                self._save_to_file(operation_name, elapsed_time)
                
                if self.verbose:
                    formatted_time = self._format_time(elapsed_time)
                    print(f"[Timer] {operation_name} завершен с ошибкой {e}. Время: {formatted_time}")
                
                raise e
        
        return wrapper
    
    def get_stats(self) -> dict:
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if not logs:
                return {}
            
            relevant_logs = logs
            if self.name:
                relevant_logs = [log for log in logs if log.get('name') == self.name]
            
            if not relevant_logs:
                return {}
            
            times = [log['elapsed_time'] for log in relevant_logs]
            
            return {
                'count': len(relevant_logs),
                'min': min(times),
                'max': max(times),
                'average': sum(times) / len(times),
                'total': sum(times)
            }
            
        except Exception as e:
            print(f"Ошибка при чтении статистики: {e}")
            return {}

"""
тест Timer с сохранением в файл
if __name__ == "__main__":
    print("=== Демонстрация Timer ===")
    
    # Тест 1: Контекстный менеджер с разными настройками
    print("\n1. Контекстный менеджер:")
    with Timer(name="test_context", unit="milliseconds") as timer:
        time.sleep(0.1)
        result = sum(i**2 for i in range(1000))
    
    print(f"Результат вычислений: {result}")
    
    # Тест 2: Декоратор
    print("\n2. Декоратор:")
    
    @Timer(name="heavy_calculation", unit="milliseconds")
    def heavy_calculation(n: int) -> int:
        #Тяжелые вычисления
        time.sleep(0.05)
        return sum(i**3 for i in range(n))
    
    result = heavy_calculation(500)
    print(f"Результат: {result}")
    
    # Тест 3: Декоратор с ошибкой
    print("\n3. Декоратор с ошибкой:")
    
    @Timer(name="failing_function", unit="milliseconds")
    def failing_function():
        time.sleep(0.01)
        raise ValueError("Искусственная ошибка!")
    
    try:
        failing_function()
    except ValueError as e:
        print(f"Поймана ошибка: {e}")
    
    # Тест 4: Разные единицы измерения
    print("\n4. Разные единицы измерения:")
    
    with Timer(name="micro_test", unit="microseconds", verbose=True) as t:
        time.sleep(0.001)
    
    with Timer(name="minute_test", unit="minutes", verbose=True) as t:
        time.sleep(0.1)
    
    # Тест 5: Статистика
    print("\n5. Статистика:")
    stats_timer = Timer(name="heavy_calculation")
    stats = stats_timer.get_stats()
    print(f"Статистика для heavy_calculation: {stats}")
    
    # Тест 6: Без вывода (verbose=False)
    print("\n6. Тихий режим (verbose=False):")
    with Timer(name="silent_test", verbose=False) as t:
        time.sleep(0.05)
    print("Тихий режим завершен (ничего не вывелось)")
    
    print("\n=== Проверка файла логов ===")
    try:
        with open("base/practice/timer_logs.json", 'r', encoding='utf-8') as f:
            logs = json.load(f)
        print(f"Всего записей в логе: {len(logs)}")
        print("Последние 2 записи:")
        for log in logs[-2:]:
            print(f"  - {log['name']}: {log['elapsed_time']:.6f}s")
    except Exception as e:
        print(f"Ошибка при чтении логов: {e}")
        
"""


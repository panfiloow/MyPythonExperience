"""
Объектно-ориентированное программирование (ООП) - парадигма программирования, в которой программа представляется как набор объектов, взаимодействующих друг с другом.

Класс - это шаблон для создания объектов. Он определяет:

Атрибуты (данные) - переменные, принадлежащие объекту

Методы (функции) - действия, которые может выполнять объект

Объект (экземпляр) - конкретная реализация класса.

 
"""


#2. Создание простого класса
class Dog:
    # Атрибут класса (общий для всех экземпляров)
    species = "Canis familiaris"
    
    def __init__(self, name, age):
        # Атрибуты экземпляра (уникальные для каждого объекта)
        self.name = name
        self.age = age
    
    # Метод экземпляра
    def description(self):
        return f"{self.name} is {self.age} years old"
    
    # Еще один метод
    def speak(self, sound):
        return f"{self.name} says {sound}"

# Создание объектов (экземпляров класса)
dog1 = Dog("Buddy", 3)
dog2 = Dog("Molly", 5)

print(dog1.description())  # Buddy is 3 years old
print(dog2.speak("Woof!"))  # Molly says Woof!
print(f"Species: {Dog.species}")  # Species: Canis familiaris


#3. Конструктор __init__
# Метод __init__ вызывается автоматически при создании нового объекта. Он инициализирует атрибуты объекта.

class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.odometer_reading = 0  # Значение по умолчанию
    
    def get_description(self):
        return f"{self.year} {self.brand} {self.model}"

my_car = Car("Toyota", "Camry", 2022)
print(my_car.get_description())  # 2022 Toyota Camry

# 4. Атрибуты класса vs атрибуты экземпляра

class Employee:
    # Атрибут класса
    company = "Tech Corp"
    employee_count = 0
    
    def __init__(self, name, salary):
        # Атрибуты экземпляра
        self.name = name
        self.salary = salary
        Employee.employee_count += 1  # Изменяем атрибут класса
    
    def display_info(self):
        return f"{self.name} works at {self.company} and earns ${self.salary}"

# Использование
emp1 = Employee("Alice", 50000)
emp2 = Employee("Bob", 60000)

print(emp1.display_info())  # Alice works at Tech Corp and earns $50000
print(emp2.display_info())  # Bob works at Tech Corp and earns $60000
print(f"Total employees: {Employee.employee_count}")  # Total employees: 2

# Изменение атрибута класса влияет на все экземпляры
Employee.company = "New Tech Corp"
print(emp1.display_info())  # Alice works at New Tech Corp and earns $50000

#5. Инкапсуляция и методы доступа
# Инкапсуляция - сокрытие внутренней реализации и предоставление контролируемого доступа.

class BankAccount:
    def __init__(self, account_holder, balance):
        self.account_holder = account_holder
        self._balance = balance  # Защищенный атрибут (соглашение)
        self.__account_id = 12345  # Приватный атрибут
    
    # Геттер (метод для получения значения)
    def get_balance(self):
        return self._balance
    
    # Сеттер (метод для установки значения с проверкой)
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False
    
    # Использование property для более Pythonic подхода
    @property
    def balance(self):
        return self._balance
    
    @balance.setter
    def balance(self, value):
        if value >= 0:
            self._balance = value
        else:
            print("Balance cannot be negative")
            
# Использование
account = BankAccount("John", 1000)
print(account.get_balance())  # 1000
account.deposit(500)
print(account.balance)  # 1500 (используем property)
account.balance = 2000  # Используем setter
print(account.balance)  # 2000

# Попытка доступа к приватному атрибуту
# print(account.__account_id)  # Ошибка!
print(account._BankAccount__account_id)  # Так можно, но не нужно

#6. Наследование
# Наследование позволяет создавать новый класс на основе существующего.

# Базовый класс
class Animal:
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def speak(self):
        return "Some sound"
    
    def info(self):
        return f"{self.name} is a {self.species}"

# Дочерний класс
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Dog")  # Вызов конструктора родителя
        self.breed = breed
    
    # Переопределение метода
    def speak(self):
        return "Woof!"
    
    def info(self):
        return f"{super().info()}, breed: {self.breed}"

# Еще один дочерний класс
class Cat(Animal):
    def __init__(self, name, color):
        super().__init__(name, "Cat")
        self.color = color
    
    def speak(self):
        return "Meow!"
    
    def info(self):
        return f"{super().info()}, color: {self.color}"

# Использование
animals = [
    Dog("Buddy", "Golden Retriever"),
    Cat("Whiskers", "Black")
]

for animal in animals:
    print(f"{animal.info()} - Sound: {animal.speak()}")
    
#7. Полиморфизм
# Полиморфизм - возможность использования объектов разных классов с одинаковым интерфейсом.

class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Circle:
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

# Полиморфизм в действии
shapes = [Rectangle(4, 5), Circle(3)]

for shape in shapes:
    print(f"Area: {shape.area():.2f}, Perimeter: {shape.perimeter():.2f}")
    
#8. Множественное наследование

class Flyable:
    def fly(self):
        return "I can fly!"

class Swimmable:
    def swim(self):
        return "I can swim!"

class Duck(Flyable, Swimmable):
    def __init__(self, name):
        self.name = name
    
    def quack(self):
        return "Quack!"

duck = Duck("Donald")
print(duck.fly())   # I can fly!
print(duck.swim())  # I can swim!
print(duck.quack()) # Quack!

# 9. Магические методы (Dunder methods)

class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages
    
    # Магический метод для строкового представления
    def __str__(self):
        return f"'{self.title}' by {self.author}"
    
    # Магический метод для официального представления
    def __repr__(self):
        return f"Book('{self.title}', '{self.author}', {self.pages})"
    
    # Магический метод для длины
    def __len__(self):
        return self.pages
    
    # Магический метод для сравнения
    def __eq__(self, other):
        if isinstance(other, Book):
            return (self.title == other.title and 
                   self.author == other.author)
        return False
    
    # Магический метод для сложения
    def __add__(self, other):
        if isinstance(other, Book):
            return Book(
                f"Collection: {self.title} & {other.title}",
                "Various Authors",
                self.pages + other.pages
            )
        return NotImplemented

# Использование
book1 = Book("Python Basics", "John Doe", 300)
book2 = Book("Advanced Python", "Jane Smith", 400)

print(str(book1))    # 'Python Basics' by John Doe
print(repr(book1))   # Book('Python Basics', 'John Doe', 300)
print(len(book1))    # 300
print(book1 == book2)  # False

collection = book1 + book2
print(collection)    # 'Collection: Python Basics & Advanced Python' by Various Authors

# 10. Статические методы и методы класса

class MathOperations:
    PI = 3.14159
    
    def __init__(self, value):
        self.value = value
    
    # Обычный метод экземпляра
    def square(self):
        return self.value ** 2
    
    # Метод класса - работает с классом, а не с экземпляром
    @classmethod
    def from_string(cls, string_value):
        return cls(float(string_value))
    
    # Статический метод - не получает ни self, ни cls
    @staticmethod
    def circle_area(radius):
        return MathOperations.PI * radius ** 2
    
    @classmethod
    def get_pi(cls):
        return cls.PI

# Использование
obj1 = MathOperations(5)
print(obj1.square())  # 25

# Создание объекта через метод класса
obj2 = MathOperations.from_string("10.5")
print(obj2.square())  # 110.25

# Использование статического метода
print(MathOperations.circle_area(3))  # 28.27431
print(obj1.circle_area(3))  # 28.27431 (можно вызывать от экземпляра)

print(MathOperations.get_pi())  # 3.14159

# 11. Абстрактные классы
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass
    
    @abstractmethod
    def perimeter(self):
        pass
    
    # Обычный метод в абстрактном классе
    def description(self):
        return "This is a shape"

class ConcreteShape(Shape):
    def __init__(self, side):
        self.side = side
    
    def area(self):
        return self.side ** 2
    
    def perimeter(self):
        return 4 * self.side

# shape = Shape()  # Ошибка! Нельзя создать экземпляр абстрактного класса
square = ConcreteShape(5)
print(square.area())       # 25
print(square.perimeter())  # 20
print(square.description())  # This is a shape

# 12. Композиция vs Наследование
# Композиция - создание объектов внутри других объектов.
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower
    
    def start(self):
        return "Engine started"

class Wheels:
    def __init__(self, count):
        self.count = count
    
    def rotate(self):
        return "Wheels rotating"

class Car:
    def __init__(self, brand, horsepower):
        self.brand = brand
        self.engine = Engine(horsepower)  # Композиция
        self.wheels = Wheels(4)          # Композиция
    
    def drive(self):
        return f"{self.brand}: {self.engine.start()}, {self.wheels.rotate()}"

my_car = Car("Toyota", 150)
print(my_car.drive())  # Toyota: Engine started, Wheels rotating


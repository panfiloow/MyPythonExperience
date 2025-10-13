""" 
1. Функции в Python
Функция - это блок кода, который выполняется только тогда, когда его вызывают.


#def имя_функции(параметры):
#    Строка документации (docstring)
#    # тело функции
#    return результат

"""

#пример
def greet(name):
    """Функция приветствия"""
    return f"Привет, {name}!"

""" 
2. Аргументы функции
Позиционные аргументы:

def power(base, exponent):
    return base ** exponent

print(power(2, 3))  # 8


Именованные аргументы:
print(power(base=2, exponent=3))  # 8
print(power(exponent=3, base=2))  # 8

Аргументы по умолчанию:
def greet(name, greeting="Привет"):
    return f"{greeting}, {name}!"

print(greet("Максим"))  # Привет, Максим!
print(greet("Мария", "Здравствуй"))  # Здравствуй, Мария!


Произвольное количество аргументов:

# *args - произвольное количество позиционных аргументов
def sum_all(*args):
    return sum(args)

print(sum_all(1, 2, 3, 4))  # 10

# **kwargs - произвольное количество именованных аргументов
def print_info(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

print_info(name="Иван", age=25, city="Москва")



3. Рекурсия в Python
Рекурсия - когда функция вызывает саму себя.

Базовые случаи:
Базовый случай - условие выхода из рекурсии

Рекурсивный случай - вызов функции самой себя

Пример: факториал
def factorial(n):
    if n == 0 or n == 1:  # базовый случай
        return 1
    else:  # рекурсивный случай
        return n * factorial(n - 1)

print(factorial(5))  # 120

4. Lambda-функции
Lambda-функции - анонимные функции, определяемые в одной строке.

Синтаксис:
lambda аргументы: выражение

# Простая lambda-функция
square = lambda x: x ** 2
print(square(5))  # 25

# Lambda с несколькими аргументами
multiply = lambda x, y: x * y
print(multiply(3, 4))  # 12

# Использование с filter()
numbers = [1, 2, 3, 4, 5, 6]
even_numbers = list(filter(lambda x: x % 2 == 0, numbers))
print(even_numbers)  # [2, 4, 6]

# Использование с map()
squared = list(map(lambda x: x ** 2, numbers))
print(squared)  # [1, 4, 9, 16, 25, 36]

# Использование с sorted()
names = ["Анна", "Петр", "Мария", "Иван"]
sorted_names = sorted(names, key=lambda x: len(x))
print(sorted_names)  # ['Иван', 'Анна', 'Петр', 'Мария']

5. Импорт модулей
Импорт всего модуля:
import math
print(math.sqrt(16))  # 4.0

from math import sqrt, pi
print(sqrt(9))  # 3.0
print(pi)       # 3.141592653589793

Импорт с псевдонимом:
import numpy as np
from math import factorial as fact

print(fact(5))  # 120

Создание собственного модуля:
my_module.py:
def hello():
    return "Привет из моего модуля!"

def add(a, b):
    return a + b

main.py:
import my_module

print(my_module.hello())  # Привет из моего модуля!
print(my_module.add(2, 3))  # 5

"""




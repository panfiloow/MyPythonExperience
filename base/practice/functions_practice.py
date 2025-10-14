""" 
Задача 1 (легкая)
Напишите функцию, которая принимает список чисел и возвращает их сумму.
"""

def my_sum(numbers):
    """Вычисляет сумму элементов списка.

    Args:
        numbers (list): Список чисел (int или float)

    Returns:
        int/float: Сумма всех элементов списка
        
    Raises:
        TypeError: Если аргумент не является списком
    
    Examples:
        >>> my_sum([1, 2, 3])
        6
        >>> my_sum([1.5, 2.5, 3.0])
        7.0
    """
    if not isinstance(numbers, list):
        raise TypeError("Аргумент должен быть списком")
    return sum(numbers)



"""
Задача 2 (легкая)
Напишите функцию, которая проверяет, является ли слово палиндромом.
"""

def isPalindrome(word):
    """Проверяет является ли слово палиндромом
    Args:
        word (str): Слово для проверки
    Returns:
        bool:  True-слово палиндром False-слово не палидром
    Raises:
        TypeError: Если аргумент не является строкой
    Examples:
        >>> isPalindrome("абоба")
        True
        >>> isPalindrome("abcd")
        False
    """
    if not isinstance(word, str):
        raise TypeError("Аргумент должен быть строкой")
    isPalindrome = True
    if word != word[::-1]: 
        isPalindrome = False
    return isPalindrome


"""
Задача 3 (средняя)
Создайте функцию, которая принимает произвольное количество чисел и возвращает кортеж из минимального и максимального значения.
"""
def find_min_max(*args):
    """Находит минимум и максимум у произвольного кол-ва чисел
    Args:
        *args (int/float): Произвольное количество чисел (int или float)
    Returns:
        tuple: Кортеж в формате (минимум, максимум)
    Raises:
        TypeError: Если хотя бы один аргумент не является int или float
        ValueError: Если не передано ни одного аргумента
    Examples:
        >>> find_min_max(1,2,3,4,5)
        (1,5)
    """
    if len(args) == 0:
        raise ValueError("Функция должна получить хотя бы один аргумент")
    for arg in args:
        if not isinstance(arg, (int, float)):
            raise TypeError(f"Все аргументы должны быть числами. Получен: {type(arg)}")
    return (min(args), max(args))

"""
Задача 4 (средняя)
Напишите рекурсивную функцию для вычисления суммы цифр числа.
"""
def digit_sum(number):
    """Считает сумму цифр целого числа

    Args:
        number (int): Произвольное целое число

    Raises:
        TypeError: Если передан не int аргумент
    Returns:
        int: Сумма цифр числа number
    """
    if not isinstance(number, int):
        raise TypeError("Аргумент должен быть int")
    return sum(map(int, str(number)))


def digit_sum_recursive(n):
    """Рекурсивно считает сумму цифр числа

    Args:
        n (int): Целое число для которого считается сумма цифр

    Raises:
        ValueError: Если не был передан аргумент
        TypeError: Если аргумент не является int

    Returns:
        int: Сумма цифр числа n 
    """
    if not isinstance(n, int):
        raise TypeError("Аргумент должен быть int")
    n = abs(n)
    if n < 10:
        return n
    else:
        return(n % 10) + digit_sum_recursive(n // 10)
    

"""
Задача 5 (средняя)
Создайте lambda-функцию, которая проверяет, является ли число четным, и используйте ее с функцией filter для фильтрации списка чисел.
"""
#is_even = lambda x: x % 2 == 0 созданная лямбда функция
#numbers = [1,2,3,4,5,6,7,8,9,10]
#even_numbers = list(filter(is_even, numbers))
#print(even_numbers)

def filter_even_numbers(numbers):
    """Из исходного списка с числами получает список четных

    Args:
        numbers (list): Список чисел int/float
    Raises:
        TypeError: Если в списке есть хотя бы один элемент не int/float

    Returns:
        list: Список четных чисел
    Examples:
        >>> filter_even_numbers([1,2,3,4])
        [2,4]
        >>> filter_even_numbers([1])
        []
    """
    if not all(isinstance(x, (int, float)) for x in numbers):
        raise TypeError("Все элементы должны быть числами")
    
    is_even = lambda x: x % 2 == 0
    return list(filter(is_even, numbers))




"""
Задача 6 (средняя)
Напишите функцию, которая принимает строку и возвращает словарь с количеством каждого символа в строке.

"""
def char_count(my_string):
    """Считает кол-во каждого символа в строке

    Args:
        my_string (str): Произвольная строка

    Raises:
        TypeError: Если аргумент не str

    Returns:
        dict: Словарь с количеством каждого символа в строке {symbol: count}
    Examples:
        >>> char_count("Абва")
        {'А': 1, 'б': 1, 'в': 1, 'а': 1}
        >>> char_count("12 4")
        {'1': 1, '2': 1, ' ': 1, '4': 1}
    """    
    if not isinstance(my_string, str):
        raise TypeError("Аргумент должен быть строкой")
    char_counts = {}
    for char in my_string:
        if char in char_counts:
            char_counts[char] += 1
        else:
            char_counts[char] = 1
    return char_counts

#from collections import Counter
#
#def char_count_counter(my_string):
#    """Версия с использованием collections.Counter"""
#    if not isinstance(my_string, str):
#        raise TypeError("Аргумент должен быть строкой")
#    
#    return dict(Counter(my_string))


"""
Задача 7 (сложная)
Создайте функцию-декоратор, который измеряет время выполнения функции.

"""
import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@timer
def my_test_timer_func():
    time.sleep(1)
    return "Функция завершена!"


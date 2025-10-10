''' 
https://pydocs.ru/peremennye-i-konstanty-v-python/ - переменные и константы
https://pydocs.ru/chisla-v-python-3/ - числа 
https://pydocs.ru/rabota-so-spiskami-v-python/ - списки 

'''
#импорты для чисел
from decimal import Decimal as D # точные вычисления для float чисел
import math # модуль математики
import fractions # дроби 
from fractions import Fraction as F
import random as rand

#импорты для списков


intVariable = 10
floatVariable = 4.5 
complexVariable = 5 + 6j
notDecimalOperation = 1.1 + 1.2
decimalOperation = D('1.1') + D('1.2')
fractionVariable = F(7, 11) # первый параметр числитель, второй знаменатель

print("Блок чисел: ")

print("Целое число: ", intVariable)
print("Float число: ", floatVariable)
print("Комплексное число: ", complexVariable)
print("Вычисление без Decimal: ", notDecimalOperation)
print("Вычисление c Decimal: ", decimalOperation)
print("Дробь: ", fractionVariable)
print("Целое число тип: ", type(intVariable))
print("Float число тип: ", type(floatVariable))
print("Комплексное число: ", type(complexVariable))
print("Равно ли обычная операция с Decimal: ", notDecimalOperation == decimalOperation )
print("Тип дроби: ", type(fractionVariable))
print("Приведение типов int -> float:", float(intVariable))
print("Модуль math (квадратный корень числа 9):", math.sqrt(9))
print("Модуль random (четные числа до 10)", rand.randrange(0, 10, 2)) # четные числа до 10
print("\n\n\n\n")

print("Блок списков: ")
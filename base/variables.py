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


print("Блок чисел: ")

intVariable = 10
floatVariable = 4.5 
complexVariable = 5 + 6j
notDecimalOperation = 1.1 + 1.2
decimalOperation = D('1.1') + D('1.2')
fractionVariable = F(7, 11) # первый параметр числитель, второй знаменатель


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
'''
append() - Добавить элемент в конец списка
extend() - Добавить все элементы списка в другой список
insert() - Вставить элемент в определенный индекс
remove() - Удаляет элемент из списка.
pop() - Удаляет и возвращает элемент с заданным индексом
clear() - Удаляет все элементы из списка
index() - Возвращает индекс первого совпадающего элемента
count() - Возвращает количество элементов, переданных в качестве аргумента
sort() - Сортировка элементов в списке в порядке возрастания
reverse() - Обратный порядок элементов в списке
'''


list = [] #пустой список 
list2 = [1,2,3,4] #int список
list3 = [1,2,'hello world', 3.5] #список с комбинированными данными
list4 = [1, 2, [4, 5]] # cписок со вложенным списком
my_list = ['p','r','o','b','e']
print("Первое значение списка list2 по индексу 0: ", list2[0])
print("Из list4 второе значение вложенного списка: ", list4[2][1])
print(my_list[-1]) # последний элемент списка 
my_list = ['p','y','d','o','c','s','.','r','u']

print( "Срез списка с помощью ':' ", my_list[2:5]) # ['d','o',c] - элементы от 2 до 5 
# Если мы хотим добавить один элемент, используем метод append(), если хотим добавить несколько элементов, то метод extend().
print(list)
list.append(1)
print(list)
list.extend([5,4,2,5,1,2,5,[34,2,4,3]])
print(list)

#оператор +, с помощью него, можно объединить два списка. 
#оператор *, который повторит элемент в списке указанное количество раз
concatlist = list + list2
print(concatlist)
multilist = list2 * 5
print(multilist)
#Для удаление используется ключевое слово del.
print(list2)
del list2[2]
print(list2)

#мы так же можем воспользоваться методами списка. 
#Метод remove(), для удаление элемента, или метод pop() для удаления элемента с заданным индексом.
#Метод pop() удаляет и возвращает последний элемент если не указан индекс. 
#Так же для очистки всего списка, мы можем воспользоваться методом clear().
list2.remove(1)
print(list2)
print(list2.pop(0))
print(list2.clear())

indexList = [0,1,2,3,4,5,6,7,8,9]
print(indexList.index(5))
indexList.insert(0, 9)
print(indexList)
print(indexList.index(5))
indexList.sort()
print(indexList)
indexList.reverse()
print(indexList)

#Генерация списков
generateList = [2**x for x in range(0, 10)]
print(generateList)
generateList2 = [2**x for x in range(20) if (2**x > 10) and (2**x < 128)]
print(generateList2)

#проверка наличия элемента
list = ['p','r','o','b','l','e','m']
print('p' in list)
print('a' in list)
print('c' not in list)
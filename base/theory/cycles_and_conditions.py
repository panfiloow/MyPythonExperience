"""
1. Конструкция if...else
Конструкция if...else позволяет выполнять код в зависимости от условий.

if условие1:
    # код, если условие1 True
elif условие2:
    # код, если условие2 True
else:
    # код, если все условия False 
"""

test_var = 10
if test_var % 3 == 0:
    print("if")
elif test_var % 3 == 1:
    print("elif")
else:
    print("else")
    
""" 
2. Цикл For
Цикл for используется для итерации по последовательностям (списки, строки, словари и т.д.).

Синтаксис:
for элемент in последовательность:
    # код для выполнения
"""
string_var = "1234567"
list_var = [1,2,3,4,5,67,[1,2,3]]


for letter in string_var:
    print(letter)

for list_item in list_var:
    print(list_item)
    if(type(list_item)==list):
        for sub_list_item in list_item:
            print(f"Элемент вложенного списка: {sub_list_item}")
            
""" 
3. Цикл While
Цикл while выполняет код, пока условие истинно.

Синтаксис:
python
while условие:
    # код для выполнения
"""

# Простой while
count = 0
while count < 5:
    print(count)
    count += 1

# Бесконечный цикл с break
while True:
    user_input = input("Введите 'стоп' для выхода: ")
    if user_input.lower() == 'стоп':
        break
    
"""
4. Операторы break и continue
break - полностью прерывает выполнение цикла

continue - пропускает текущую итерацию и переходит к следующей 
"""

# break
for i in range(10):
    if i == 5:
        break
    print(i)  # Выведет: 0, 1, 2, 3, 4

# continue
for i in range(5):
    if i == 2:
        continue
    print(i)  # Выведет: 0, 1, 3, 4
    
"""
5. Оператор Pass
pass - оператор-заглушка, который ничего не делает. Используется когда синтаксис требует наличия кода, но вам не нужно выполнять никаких действий.
"""
# Заглушка в условии
x = 10
if x > 5:
    pass  # Позже добавлю код
else:
    print("x меньше или равно 5")
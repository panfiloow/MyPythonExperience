#Легкая задача:
#Задача: Создайте список из 5 чисел. Найдите сумму всех чисел в списке и выведите результат.

numbers = [1, 2, 3, 4, 5]
# Ожидаемый результат: 15
print("Сумма чисел numbers: ", sum(numbers))

#Средняя задача:
#Задача: Создайте словарь, где ключами будут имена людей, а значениями — их возраст. Напишите функцию, которая принимает этот словарь и возвращает имя самого старшего человека.
peoplesDict = {
    "Иван": 20,
    "Газонюх": 10,
    "Алеша": 47
}
### моя функция
def searchMaxAge(dict):
    max_age = 0
    for name, age in dict.items():
        if age > max_age:
            retValue = name
    return retValue

### от гпт
def searchMaxAgeGpt(dict):
    if not dict:  
        return None
    return max(dict, key=dict.get)
### отличия, моя ломается при пустом списке
### Gpt использовал функцию max которая работает со словарями, тем самым упростив код

print(searchMaxAge(peoplesDict))
print(searchMaxAgeGpt(peoplesDict))
#Сложная задача:
#Задача: Напишите функцию, которая принимает список строк и возвращает новый список, содержащий только уникальные строки (без повторений), 
#отсортированные по длине строки (от короткой к длинной). Если длины строк одинаковые, сортируйте их в алфавитном порядке.

strings = ["apple", "banana", "pear", "apple", "kiwi", "banana"]
# Ожидаемый результат: ['kiwi', 'pear', 'apple', 'banana']

def myStringFunc(myStr):
    myStr = list(set(myStr))
    myStr.sort(key=lambda x: (len(x), x))
    return myStr

print(myStringFunc(strings))
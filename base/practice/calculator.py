"""Простой калькулятор"""

while True:
    try:
        expression = input("Введите выражение (или 'exit' для выхода): ")
        if expression.lower() == 'exit':
            break
        result = eval(expression)
        print(f"Результат: {result}")
    except:
        print("Ошибка! Проверьте выражение")
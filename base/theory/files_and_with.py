# 1. Работа с файлами (чтение/запись)
# Чтение файлов

# Открытие файла для чтения
file = open('file.txt', 'r')  # 'r' - режим чтения
content = file.read()
file.close()

# Режимы открытия файлов:
# 'r' - чтение (по умолчанию)
# 'w' - запись (перезаписывает файл)
# 'a' - добавление в конец файла
# 'r+' - чтение и запись
# 'b' - бинарный режим (например, 'rb', 'wb')

# Запись в файлы

# Запись в файл (перезаписывает существующий)
file = open('file.txt', 'w')
file.write("Hello, World!\n")
file.write("Second line")
file.close()

# Добавление в файл
file = open('file.txt', 'a')
file.write("\nAppended text")
file.close()

# 2. Контекстные менеджеры (with)
# Контекстные менеджеры автоматически закрывают файлы и освобождают ресурсы.

# Автоматическое закрытие файла
with open('file.txt', 'r') as file:
    content = file.read()
    # Файл автоматически закроется после выхода из блока with

# Работа с несколькими файлами
with open('input.txt', 'r') as input_file, open('output.txt', 'w') as output_file:
    data = input_file.read()
    output_file.write(data.upper())
    
# 3. Обработка исключений (try/except/finally)

try:
    # Код, который может вызвать исключение
    result = 10 / 0
except ZeroDivisionError:
    # Обработка конкретного исключения
    print("Деление на ноль!")
except (TypeError, ValueError) as e:
    # Обработка нескольких исключений
    print(f"Ошибка типа или значения: {e}")
except Exception as e:
    # Обработка всех остальных исключений
    print(f"Неизвестная ошибка: {e}")
else:
    # Выполняется, если исключений не было
    print("Операция выполнена успешно")
finally:
    # Выполняется всегда
    print("Блок finally выполнен")
    
# Обработка исключений при работе с файлами
try:
    with open('nonexistent.txt', 'r') as file:
        content = file.read()
except FileNotFoundError:
    print("Файл не найден!")
except PermissionError:
    print("Нет прав доступа к файлу!")
except IOError as e:
    print(f"Ошибка ввода-вывода: {e}")
    
# 4. Создание собственных исключений

# Базовое пользовательское исключение
class MyCustomError(Exception):
    """Мое пользовательское исключение"""
    pass

# Исключение с дополнительной информацией
class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)
    
    def __str__(self):
        if self.field:
            return f"Ошибка валидации в поле '{self.field}': {self.message}"
        return f"Ошибка валидации: {self.message}"

# Исключения с наследованием
class NegativeNumberError(ValueError):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Отрицательное число не допускается: {value}")

# Использование пользовательских исключений
def process_positive_number(number):
    if number < 0:
        raise NegativeNumberError(number)
    return number * 2

try:
    process_positive_number(-5)
except NegativeNumberError as e:
    print(f"Поймано исключение: {e}")
    
# Полный пример с пользовательскими исключениями
class FileProcessingError(Exception):
    """Базовое исключение для обработки файлов"""
    pass

class FileEmptyError(FileProcessingError):
    """Файл пуст"""
    pass

class InvalidFormatError(FileProcessingError):
    """Неверный формат данных"""
    def __init__(self, line_number, content):
        self.line_number = line_number
        self.content = content
        super().__init__(f"Неверный формат в строке {line_number}: {content}")

def process_data_file(filename):
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
            
            if not lines:
                raise FileEmptyError("Файл не содержит данных")
            
            for i, line in enumerate(lines, 1):
                if not line.strip().isdigit():
                    raise InvalidFormatError(i, line.strip())
                    
    except FileNotFoundError:
        raise FileProcessingError(f"Файл {filename} не найден")
    except PermissionError:
        raise FileProcessingError(f"Нет прав доступа к файлу {filename}")
import datetime
import logging
import os
from pathlib import Path
import re
import shutil
from typing import Optional, Tuple
# Задача 1 (Начальный уровень)
# Чтение и анализ текстового файла
# Напишите программу, которая читает текстовый файл и выводит:

# Общее количество строк
# Общее количество слов
# Самую длинную строку в файле
# Обработайте исключения: FileNotFoundError, PermissionError.

def first_task() -> None:
    file_path = Path(r'base\practice\testfile.txt')
    
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
    except FileNotFoundError:
        print(f"Ошибка! Файл {file_path} не найден")
        return
    except PermissionError:
        print("Ошибка нет доступа к файлу")
        return
    except Exception as e:
        print(f"Неожиданная ошибка {e}")
        return
    
    if not lines:
        print("Файл пуст")
        return
    
    total_lines = len(lines)
    total_words : int = 0
    max_length : int = 0
    longest_line_index : int = 0
    longest_line_content : str = ""
    
    for i, line in enumerate(lines):
        words = line.split()
        total_words += len(words)
        current_length = len(line.rstrip('\n'))
        if current_length > max_length:
            max_length = current_length
            longest_line_index = i + 1
            longest_line_content = line.rstrip('\n')
            
        total_words += len(words)
        

    print(f"Общее количество строк в файле: {total_lines}")
    print(f"Общее количество слов: {total_words}")
    print(f"Самая длинная строка №{longest_line_index}, содержит символов: {max_length}")
    print(f"Содержимое: '{longest_line_content}'")
    
# Задача 2 (Начальный уровень)
# Журнал ошибок
# Создайте программу, которая запрашивает у пользователя число и записывает в файл calculations.txt результат его деления на 2.
# Если пользователь вводит не число или происходит деление на ноль, программа должна записывать информацию об ошибке в файл error_log.txt с указанием даты и времени ошибки.

def second_task() -> None:
    calculation_path = Path(r'base\practice\calculation.txt')
    error_log_path = Path(r'base\practice\error_log.txt')
    
    calculation_path.parent.mkdir(parents=True, exist_ok=True)
    error_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    def log_error(error_type: str, message: str) -> None:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(error_log_path, 'a', encoding='utf-8') as error_log:
                error_log.write(f"[{timestamp}] {error_type}: {message}\n")
        except Exception as log_e:
            print(f"Не удалось записать в лог ошибок: {log_e}")
    
    def log_calculation(number: str, result: float) -> None:
        try:
            with open(calculation_path, 'a', encoding='utf-8') as calculation_log:
                calculation_log.write(f"Число: {number}, Результат : {result}\n")
        except Exception as calc_e:
            log_error("FileWriteError", f"Не удалось записать расчет: {calc_e}")
    
    try:
        user_input = input("Введите число на которое поделится 2: ")
        number = float(user_input)
        result = 2 / number
        
        log_calculation(user_input, result)
        print(f"Результат: {result} (записано в {calculation_path})")
        
    except ValueError:
        error_msg = f"Некорректный ввод: '{user_input}' - должно быть числом"
        print(f"Ошибка ввода: {error_msg}")
        log_error("ValueError", error_msg)
            
    except ZeroDivisionError:
        error_msg = f"Попытка деления на ноль для ввода: '{user_input}'"
        print(f"Ошибка деления: {error_msg}")
        log_error("ZeroDivisionError", error_msg)
        
    except Exception as e:
        error_msg = f"Неожиданная ошибка при обработке ввода '{user_input}': {e}"
        print(f"Произошла ошибка: {error_msg}")
        log_error("UnexpectedError", error_msg)

# Задача 3 (Средний уровень)
# Валидатор конфигурационного файла
# Напишите программу, которая читает конфигурационный файл в формате:

# ключ=значение
# Создайте собственные исключения:

# InvalidConfigFormatError - для строк с неправильным форматом
# DuplicateKeyError - для повторяющихся ключей
# EmptyValueError - для ключей с пустыми значениями
# Программа должна проверять файл и выбрасывать соответствующие исключения.

def third_task() -> None:
    
    class InvalidConfigFormatError(Exception):
        
        def __init__(self, line_number: int, content: str):
            self.line_number = line_number
            self.content = content
            super().__init__(f"Неверный формат в строке {line_number}: {content}")
    
    class DuplicateKeyError(Exception):
        
        def __init__(self, line_number: int, key: str, first_occurrence: int):
            self.line_number = line_number
            self.key = key
            self.first_occurrence = first_occurrence
            super().__init__(f"Дубликат ключа '{key}' в строке {line_number} (первое вхождение в строке {first_occurrence})")
    
    class EmptyValueError(Exception):
        
        def __init__(self, line_number: int, key: str):
            self.line_number = line_number
            self.key = key
            super().__init__(f"Пустое значение для ключа '{key}' в строке {line_number}")
    
    def parse_config_line(line, line_number) -> Tuple[Optional[str], Optional[str]]:
        
        line = line.strip()
        
        if not line or line.startswith('#'):
            return None, None
        
        pattern = r'^\s*([^=#\s]+)\s*=\s*(.*?)\s*$'
        match = re.match(pattern, line)
        
        if not match:
            raise InvalidConfigFormatError(line_number, line)
        
        key = match.group(1).strip()
        value = match.group(2).strip()
        
        return key, value
        
          
    config_file_path = Path(r'base\practice\configs\test_duplicate_keys.cfg')
    config = {}
    key_positions = {}
    
    try:
        
        with open(config_file_path, 'r', encoding='utf-8') as config_file:
            lines = config_file.readlines()
            
            for line_number, line in enumerate(lines, 1):
                try:
                    key, value = parse_config_line(line, line_number)
            
                    if key is None:
                        continue
                    
                    if key in key_positions:
                        raise DuplicateKeyError(line_number, key, key_positions[key])
                    
                    if value == "":
                        raise EmptyValueError(line_number, key)     
                    
                    config[key] = value
                    key_positions[key] = line_number           
                    
                    
                except (InvalidConfigFormatError, EmptyValueError, DuplicateKeyError) as e:
                    print(f"Ошибка валидации: {e}")
                    continue 
                
                
            print(f"Файл {config_file_path} проверен.")
                
    except FileNotFoundError:
        print(f"Файл {config_file_path} не найден")
        
    except Exception as e:
        print(f"Ошибка: {e}")
    
    

# Задача 4 (Средний уровень)
# Калькулятор с историей операций
# Реализуйте калькулятор, который:
# Читает математическое выражение от пользователя
# Вычисляет результат
# Записывает выражение и результат в файл history.txt
# Обрабатывает исключения (деление на ноль, неверный формат и т.д.)
# При запуске показывает последние 5 операций из истории
# Создайте собственные исключения для различных математических ошибок.

def fourth_task():
    
    OPERATORS = {
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '//': lambda x, y: x // y,  
        '%': lambda x, y: x % y,   
        '**': lambda x, y: x ** y   
    }
    
    class MathError(Exception):
        pass

    class DivisionByZeroError(MathError):
        def __init__(self):
            super().__init__("Ошибка: Деление на ноль")

    class InvalidExpressionError(MathError):
        def __init__(self, expression):
            super().__init__(f"Ошибка: Неверный формат выражения '{expression}'")

    class InvalidOperatorError(MathError):
        def __init__(self, operator):
            super().__init__(f"Ошибка: Неверный оператор '{operator}'")

    class CalculationError(MathError):
        def __init__(self, message):
            super().__init__(f"Ошибка вычисления: {message}")
        
    def show_last_operations(history_path):
        try:
            with open(history_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                if lines:
                    last_5_operations = lines[-5:] if len(lines) >= 5 else lines
                    print("Последние 5 операций:")
                    for operation in last_5_operations:
                        print(operation.strip())
                else:
                    print("История операций пуста")
                    
        except FileNotFoundError:
            print("Файл истории не найден. Будет создан новый")
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
    
    def save_to_history(history_path, expression, result):
        try:
            with open(history_path, 'a', encoding='utf-8') as history:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history.write(f"[{timestamp}] {expression} = {result}\n")
        except Exception as e:
            print(f"Ошибка при сохранении в историю: {e}")
            
    def parse_expression(expression):
        expression = expression.replace(' ', '')
        
        operator = None
        for op in sorted(OPERATORS.keys(), key=len, reverse=True):
            if op in expression:
                operator = op
                break
        
        if not operator:
            raise InvalidExpressionError(expression)
        
        parts = expression.split(operator, 1)
        if len(parts) != 2:
            raise InvalidExpressionError(expression)
        
        operand1_str, operand2_str = parts
        
        try:
            operand1 = float(operand1_str)
            operand2 = float(operand2_str)
        except ValueError:
            raise InvalidExpressionError(expression)
        
        return operand1, operand2, operator
    
    def calculate_expression(expression):
        operand1, operand2, operator = parse_expression(expression)
        
        if operator in ['/', '//'] and operand2 == 0:
            raise DivisionByZeroError()
        
        if operator not in OPERATORS:
            raise InvalidOperatorError(operator)
        
        try:
            result = OPERATORS[operator](operand1, operand2)
            return result
        except Exception as e:
            raise CalculationError(str(e))
    
    history_path = Path(r'base\practice\history.txt')
    
    show_last_operations(history_path)
    print("\nДоступные операторы: +, -, *, /, //, %, **")
    print("Примеры: 10 + 5, 3.5 * 2, 2 ** 3, 10 // 3")
    print("Введите 'exit' для выхода")
    
    while True:
        try:
            expression = input("Введите выражение: ").strip()
            
            if expression.lower() == 'exit':
                print("До свидания!")
                break
            
            if not expression:
                continue
            5
            result = calculate_expression(expression)
            
            print(f"Результат: {result}")
            
            save_to_history(history_path, expression, result)
            
        except DivisionByZeroError as e:
            print(e)
        except (InvalidExpressionError, InvalidOperatorError, CalculationError) as e:
            print(e)
        except Exception as e:
            print(f"Непредвиденная ошибка: {e}")
        
        
                

# Задача 5 (Продвинутый уровень)
# Система резервного копирования
# Напишите программу для создания резервных копий файлов. Программа должна:

# Принимать путь к исходной директории и путь для бэкапа
# Копировать все файлы из исходной директории в директорию бэкапа
# Создавать лог-файл с информацией о скопированных файлах и возможных ошибках
# Обрабатывать исключения (файл не найден, нет прав доступа, диск полон)
# Создавать собственные исключения для различных сценариев ошибок

# Реализуйте классы исключений:
# BackupSourceError - проблемы с исходной директорией
# BackupDestinationError - проблемы с директорией назначения
# BackupFileError - ошибки при копировании отдельных файлов
# Все исключения должны содержать подробную информацию об ошибке.

def fifth_task():
    
    class BackupError(Exception):
        pass

    class BackupSourceError(BackupError):
    
        def __init__(self, path, message="Ошибка исходной директории"):
            self.path = path
            self.message = f"{message}: {path}"
            super().__init__(self.message)

    class BackupDestinationError(BackupError):
        
        def __init__(self, path, message="Ошибка директории назначения"):
            self.path = path
            self.message = f"{message}: {path}"
            super().__init__(self.message)

    class BackupFileError(BackupError):
        
        def __init__(self, file_path, message="Ошибка копирования файла"):
            self.file_path = file_path
            self.message = f"{message}: {file_path}"
            super().__init__(self.message)

    class BackupSystem:
        def __init__(self):
            self.logger = self._setup_logger()
            self.copied_files = 0
            self.failed_files = 0
        
        def _setup_logger(self):
            logger = logging.getLogger('BackupSystem')
            logger.setLevel(logging.INFO)
            
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            
            file_handler = logging.FileHandler(f'backup_log_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.log')
            file_handler.setFormatter(formatter)
            
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
            return logger
        
        def _validate_source_directory(self, source_path):

            if not os.path.exists(source_path):
                raise BackupSourceError(source_path, "Исходная директория не существует")
            
            if not os.path.isdir(source_path):
                raise BackupSourceError(source_path, "Указанный путь не является директорией")
            
            if not os.access(source_path, os.R_OK):
                raise BackupSourceError(source_path, "Нет прав на чтение исходной директории")
        
        def _validate_destination_directory(self, dest_path):
            
            try:
                if not os.path.exists(dest_path):
                    os.makedirs(dest_path, exist_ok=True)
                    self.logger.info(f"Создана директория назначения: {dest_path}")
                
                if not os.access(dest_path, os.W_OK):
                    raise BackupDestinationError(dest_path, "Нет прав на запись в директорию назначения")
                    
            except PermissionError as e:
                raise BackupDestinationError(dest_path, f"Ошибка прав доступа: {e}")
            except OSError as e:
                raise BackupDestinationError(dest_path, f"Ошибка создания директории: {e}")
        
        def _check_disk_space(self, source_path, dest_path):
            try:
                dest_drive = os.path.splitdrive(dest_path)[0]
                disk_usage = shutil.disk_usage(dest_path)
                
                total_size = 0
                for dirpath, dirnames, filenames in os.walk(source_path):
                    for filename in filenames:
                        filepath = os.path.join(dirpath, filename)
                        try:
                            total_size += os.path.getsize(filepath)
                        except OSError:
                            continue
                
                if total_size > disk_usage.free:
                    raise BackupDestinationError(
                        dest_path, 
                        f"Недостаточно места на диске. Требуется: {total_size}, доступно: {disk_usage.free}"
                    )
                    
                self.logger.info(f"Проверка места на диске: требуется {total_size}, доступно {disk_usage.free}")
                
            except OSError as e:
                self.logger.warning(f"Не удалось проверить место на диске: {e}")
        
        def _copy_file(self, source_file, dest_file):
            try:
                dest_dir = os.path.dirname(dest_file)
                if not os.path.exists(dest_dir):
                    os.makedirs(dest_dir, exist_ok=True)
                
                shutil.copy2(source_file, dest_file)
                self.copied_files += 1
                self.logger.info(f"Успешно скопирован: {source_file} -> {dest_file}")
                
            except PermissionError as e:
                self.failed_files += 1
                raise BackupFileError(source_file, f"Ошибка прав доступа при копировании: {e}")
            except OSError as e:
                self.failed_files += 1
                raise BackupFileError(source_file, f"Системная ошибка при копировании: {e}")
            except Exception as e:
                self.failed_files += 1
                raise BackupFileError(source_file, f"Неожиданная ошибка при копировании: {e}")
        
        def _backup_directory(self, source_path, dest_path):
            try:
                for item in os.listdir(source_path):
                    source_item = os.path.join(source_path, item)
                    dest_item = os.path.join(dest_path, item)
                    
                    if os.path.isdir(source_item):
                        self._backup_directory(source_item, dest_item)
                    else:
                        try:
                            self._copy_file(source_item, dest_item)
                        except BackupFileError as e:
                            self.logger.error(e.message)
                            continue
                            
            except PermissionError as e:
                raise BackupSourceError(source_path, f"Ошибка доступа к исходной директории: {e}")
            except OSError as e:
                raise BackupSourceError(source_path, f"Ошибка чтения исходной директории: {e}")
        
        def create_backup(self, source_path, dest_path):
            self.logger.info(f"Начало резервного копирования: {source_path} -> {dest_path}")
            self.copied_files = 0
            self.failed_files = 0
            
            try:
                self._validate_source_directory(source_path)
                self.logger.info(f"Исходная директория проверена: {source_path}")
                
                self._validate_destination_directory(dest_path)
                self.logger.info(f"Директория назначения проверена: {dest_path}")
                
                self._check_disk_space(source_path, dest_path)
                
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_dir = os.path.join(dest_path, f"backup_{timestamp}")
                os.makedirs(backup_dir, exist_ok=True)
                
                self._backup_directory(source_path, backup_dir)
                
                success = self.failed_files == 0
                status = "УСПЕШНО" if success else "С ОШИБКАМИ"
                
                self.logger.info(f"Резервное копирование завершено {status}")
                self.logger.info(f"Скопировано файлов: {self.copied_files}")
                self.logger.info(f"Ошибок копирования: {self.failed_files}")
                self.logger.info(f"Путь к бэкапу: {backup_dir}")
                
                return success
                
            except BackupSourceError as e:
                self.logger.error(f"Ошибка исходной директории: {e}")
                return False
            except BackupDestinationError as e:
                self.logger.error(f"Ошибка директории назначения: {e}")
                return False
            except Exception as e:
                self.logger.error(f"Неожиданная ошибка: {e}")
                return False
    
    backup_system = BackupSystem()
    print("=== Система резервного копирования ===")
    
    try:
        source_path = input("Введите путь к исходной директории: ").strip()
        dest_path = input("Введите путь для сохранения бэкапа: ").strip()
        
        if not source_path or not dest_path:
            print("Ошибка: пути не могут быть пустыми")
            return
        
        success = backup_system.create_backup(source_path, dest_path)
        
        if success:
            print("\n✅ Резервное копирование завершено успешно!")
            print(f"Скопировано файлов: {backup_system.copied_files}")
        else:
            print("\n⚠️ Резервное копирование завершено с ошибками")
            print(f"Скопировано файлов: {backup_system.copied_files}")
            print(f"Ошибок: {backup_system.failed_files}")
            print("Подробности смотрите в лог-файле")
            
    except KeyboardInterrupt:
        print("\n\nОперация прервана пользователем")
    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")



def main():
    print("Задача 1: Чтение и анализ текстового файла")
    print("=" * 45)
    first_task()
    print("=" * 45)
    print("Задача 2: Журнал ошибок")
    print("=" * 45)
    second_task()
    print("=" * 45)
    print("Задача 3: Валидатор конфигурационного файла")
    print("=" * 45)
    third_task()
    print("=" * 45)
    print("Задача 4: Калькулятор с историей операций")
    print("=" * 45)
    fourth_task()
    print("=" * 45)
    print("Задача 5: Система резервного копирования")
    print("=" * 45)
    fifth_task()
    print("=" * 45)

if __name__ == "__main__":
    main()
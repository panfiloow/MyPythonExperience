"""
Задача 8 (очень сложная объемная)
Система управления банковскими счетами

Создайте модуль bank_system.py с следующими функциями:
create_account(account_id, initial_balance=0) - создает новый счет
deposit(account_id, amount) - пополняет счет
withdraw(account_id, amount) - снимает деньги со счета
transfer(from_account, to_account, amount) - переводит деньги между счетами
get_balance(account_id) - возвращает баланс счета
get_transaction_history(account_id) - возвращает историю операций

Требования:
Используйте словарь для хранения счетов
Каждый счет должен хранить баланс и историю операций
Реализуйте проверку на достаточность средств при снятии и переводе
История операций должна содержать тип операции, сумму, дату и время
Используйте модуль datetime для работы с датами
Создайте декоратор для логирования операций

"""
import json 
import datetime
from functools import wraps
from pathlib import Path  

ACCOUNTS_FILE = 'base/practice/bank_account_system/accounts.json'
LOG_FILE = 'base/practice/bank_account_system/operation_logs.txt'
bank_accounts = {}

def load_accounts():
    """Загружает счета из файла при запуске"""
    try:
        with open(ACCOUNTS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for account_id, account_data in data.items():
                for transaction in account_data.get('transactions', []):
                    if 'datetime' in transaction:
                        transaction['datetime'] = datetime.datetime.fromisoformat(transaction['datetime'])
            return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
        
def save_accounts():
    """Сохраняет счета в файл"""
    serializable_accounts = {}
    for account_id, account_data in bank_accounts.items():
        serializable_accounts[account_id] = account_data.copy()
        serializable_accounts[account_id]['transactions'] = []
        
        for transaction in account_data.get('transactions', []):
            transaction_copy = transaction.copy()
            if 'datetime' in transaction_copy and isinstance(transaction_copy['datetime'], datetime.datetime):
                transaction_copy['datetime'] = transaction_copy['datetime'].isoformat()
            serializable_accounts[account_id]['transactions'].append(transaction_copy)
    
    with open(ACCOUNTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(serializable_accounts, f, ensure_ascii=False, indent=2)


def write_log(message, log_type="INFO"):
    "Функция записи лога"
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_message = f"[{timestamp}] [{log_type}] {message}\n"
    
    Path(LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(log_message)

def bank_system_logger(func):
    """Декоратор для логирования функций банковской системы"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        if func_name == 'create_account':
            account_id = str(args[0]) if args else str(kwargs.get('account_id', ''))
            initial_balance = args[1] if len(args) > 1 else kwargs.get('initial_balance', 0)
            write_log(f"Попытка создания аккаунта {account_id} с балансом {initial_balance}", "INFO")
        
        elif func_name in ['deposit', 'withdraw']:
            account_id = str(args[0]) if args else str(kwargs.get('account_id', ''))
            amount = args[1] if len(args) > 1 else kwargs.get('amount', 0)
            write_log(f"Операция {func_name} для аккаунта {account_id} на сумму {amount}", "INFO")
            
        elif func_name == 'transfer':
            from_acc = str(args[0]) if args else str(kwargs.get('from_account', ''))
            to_acc = str(args[1]) if len(args) > 1 else str(kwargs.get('to_account', ''))
            amount = args[2] if len(args) > 2 else kwargs.get('amount', 0)
            write_log(f"Перевод с {from_acc} на {to_acc} сумму {amount}", "INFO")
        
        else:
            write_log(f"Вызов функции {func_name}", "INFO")
        
        try:
            result = func(*args, **kwargs)
            
            if func_name == 'create_account':
                account_id = str(args[0]) if args else str(kwargs.get('account_id', ''))
                if result:
                    write_log(f"Аккаунт {account_id} успешно создан с балансом {args[1] if len(args) > 1 else kwargs.get('initial_balance', 0)}", "SUCCESS")
                else:
                    write_log(f"Не удалось создать аккаунт {account_id} - аккаунт уже существует", "WARNING")
                    
            elif func_name == 'deposit':
                account_id = str(args[0]) if args else str(kwargs.get('account_id', ''))
                amount = args[1] if len(args) > 1 else kwargs.get('amount', 0)
                if result:
                    current_balance = get_balance(account_id)
                    write_log(f"Успешное пополнение счета {account_id} на {amount}. Текущий баланс: {current_balance}", "SUCCESS")
                else:
                    if account_id not in bank_accounts:
                        write_log(f"Ошибка пополнения: аккаунт {account_id} не существует", "ERROR")
                    elif amount <= 0:
                        write_log(f"Ошибка пополнения: неверная сумма {amount} (должна быть положительной)", "ERROR")
                    else:
                        write_log(f"Ошибка пополнения счета {account_id} на {amount} по неизвестной причине", "ERROR")
                        
            elif func_name == 'withdraw':
                account_id = str(args[0]) if args else str(kwargs.get('account_id', ''))
                amount = args[1] if len(args) > 1 else kwargs.get('amount', 0)
                if result:
                    current_balance = get_balance(account_id)
                    write_log(f"Успешное снятие {amount} со счета {account_id}. Текущий баланс: {current_balance}", "SUCCESS")
                else:
                    if account_id not in bank_accounts:
                        write_log(f"Ошибка снятия: аккаунт {account_id} не существует", "ERROR")
                    elif amount <= 0:
                        write_log(f"Ошибка снятия: неверная сумма {amount} (должна быть положительной)", "ERROR")
                    else:
                        current_balance = get_balance(account_id)
                        write_log(f"Ошибка снятия: недостаточно средств на счете {account_id}. Запрошено: {amount}, доступно: {current_balance}", "ERROR")
                        
            elif func_name == 'transfer':
                from_acc = str(args[0]) if args else str(kwargs.get('from_account', ''))
                to_acc = str(args[1]) if len(args) > 1 else str(kwargs.get('to_account', ''))
                amount = args[2] if len(args) > 2 else kwargs.get('amount', 0)
                if result:
                    from_balance = get_balance(from_acc)
                    to_balance = get_balance(to_acc)
                    write_log(f"Успешный перевод {amount} с {from_acc} на {to_acc}. Балансы: {from_acc}={from_balance}, {to_acc}={to_balance}", "SUCCESS")
                else:
                    error_details = []
                    if from_acc not in bank_accounts:
                        error_details.append(f"счет отправителя {from_acc} не существует")
                    if to_acc not in bank_accounts:
                        error_details.append(f"счет получателя {to_acc} не существует")
                    if amount <= 0:
                        error_details.append(f"неверная сумма {amount}")
                    if from_acc in bank_accounts and amount > 0:
                        from_balance = get_balance(from_acc)
                        if from_balance < amount:
                            error_details.append(f"недостаточно средств (доступно: {from_balance}, требуется: {amount})")
                    
                    error_msg = "Ошибка перевода: " + ", ".join(error_details) if error_details else "неизвестная ошибка"
                    write_log(error_msg, "ERROR")
            
            return result
            
        except Exception as e:
            write_log(f"Критическая ошибка в функции {func_name}: {str(e)}", "ERROR")
            raise
    
    return wrapper
    

@bank_system_logger
def create_account(account_id, initial_balance=0):
    account_id = str(account_id)
    if account_id in bank_accounts:
        return False  
    bank_accounts[account_id] = {'balance': initial_balance, 'transactions': []}
    save_accounts()
    return True  

@bank_system_logger
def deposit(account_id, amount):
    account_id = str(account_id)
    
    if account_id not in bank_accounts:
        return False
    
    if amount <= 0:
        return False
    
    bank_accounts[account_id]['balance'] += amount
    
    transaction = {
        'type': 'deposit',
        'amount': amount,
        'datetime': datetime.datetime.now(),
        'balance_after': bank_accounts[account_id]['balance']
    }
    bank_accounts[account_id]['transactions'].append(transaction)
    save_accounts()
    return True

@bank_system_logger
def withdraw(account_id, amount):
    account_id = str(account_id)
    
    if account_id not in bank_accounts:
        return False
    
    if amount <= 0:
        return False
    
    if bank_accounts[account_id]['balance'] < amount:
        return False
    
    bank_accounts[account_id]['balance'] -= amount
    
    transaction = {
        'type': 'withdraw',
        'amount': amount,
        'datetime': datetime.datetime.now(),
        'balance_after': bank_accounts[account_id]['balance']
    }
    bank_accounts[account_id]['transactions'].append(transaction)
    
    save_accounts()
    return True

@bank_system_logger
def transfer(from_account, to_account, amount):
    from_account = str(from_account)
    to_account = str(to_account)
    
    if from_account not in bank_accounts:
        return False
    
    if to_account not in bank_accounts:
        return False
    
    if amount <= 0:
        return False
    
    if bank_accounts[from_account]['balance'] < amount:
        return False
    
    bank_accounts[from_account]['balance'] -= amount
    bank_accounts[to_account]['balance'] += amount
    
    transaction_out = {
        'type': 'transfer_out',
        'amount': amount,
        'datetime': datetime.datetime.now(),
        'to_account': to_account,
        'balance_after': bank_accounts[from_account]['balance']
    }
    
    transaction_in = {
        'type': 'transfer_in', 
        'amount': amount,
        'datetime': datetime.datetime.now(),
        'from_account': from_account,
        'balance_after': bank_accounts[to_account]['balance']
    }
    
    bank_accounts[from_account]['transactions'].append(transaction_out)
    bank_accounts[to_account]['transactions'].append(transaction_in)
    
    save_accounts()
    return True

@bank_system_logger
def get_balance(account_id):
    account_id = str(account_id)
    
    if account_id not in bank_accounts:
        return None
    
    balance = bank_accounts[account_id]['balance']
    return balance

@bank_system_logger
def get_transaction_history(account_id):
    account_id = str(account_id)
    
    if account_id not in bank_accounts:
        return []
    
    transactions = bank_accounts[account_id]['transactions']
    return transactions

bank_accounts = load_accounts()

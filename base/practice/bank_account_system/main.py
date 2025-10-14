from bank_system import *

def show_menu():
    print("\n=== БАНКОВСКАЯ СИСТЕМА ===")
    print("1. Создать счет")
    print("2. Пополнить счет") 
    print("3. Снять средства")
    print("4. Перевести деньги")
    print("5. Проверить баланс")
    print("6. История операций")
    print("7. Выход")
    return input("Выберите действие: ")

def main():
    while True:
        choice = show_menu()
        
        if choice == '1':
            account_id = input("Введите ID счета: ")
            balance = float(input("Начальный баланс: "))
            if create_account(account_id, balance):
                print("Счет создан успешно!")
            else:
                print("Ошибка: счет уже существует!")
                
        elif choice == '2':
            account_id = input("Введите ID счета: ")
            amount = float(input("Сумма пополнения: "))
            if deposit(account_id, amount):
                print("Счет пополнен успешно!")
            else:
                print("Ошибка пополнения!")
                
        elif choice == '3':
            account_id = input("Введите ID счета: ")
            amount = float(input("Сумма снятия: "))
            if withdraw(account_id, amount):
                print("Средства сняты успешно!")
            else:
                print("Ошибка снятия!")
                
        elif choice == '4':
            from_acc = input("Счет отправителя: ")
            to_acc = input("Счет получателя: ")
            amount = float(input("Сумма перевода: "))
            if transfer(from_acc, to_acc, amount):
                print("Перевод выполнен успешно!")
            else:
                print("Ошибка перевода!")
                
        elif choice == '5':
            account_id = input("Введите ID счета: ")
            balance = get_balance(account_id)
            if balance is not None:
                print(f"Баланс счета: {balance}")
            else:
                print("Счет не найден!")
                
        elif choice == '6':
            account_id = input("Введите ID счета: ")
            history = get_transaction_history(account_id)
            if history:
                print(f"История операций ({len(history)}):")
                for i, trans in enumerate(history, 1):
                    print(f"{i}. {trans['type']}: {trans['amount']} | {trans['datetime']}")
            else:
                print("Счет не найден или нет операций!")
                
        elif choice == '7':
            print("Выход из системы...")
            break
        else:
            print("Неверный выбор!")

if __name__ == "__main__":
    main()
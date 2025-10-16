import pyautogui
import time
import sys

def auto_clicker(interval=10):
    """
    Автоматический кликер мыши
    interval: интервал между кликами в секундах
    """
    print(f"Автокликер запущен. Клики каждые {interval} секунд.")
    print("Для остановки нажмите Ctrl+C")
    
    try:
        while True:
            x, y = pyautogui.position()
            
            pyautogui.click()
            
            print(f"Клик выполнен в позиции ({x}, {y})")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\nАвтокликер остановлен.")

if __name__ == "__main__":
    auto_clicker(10)
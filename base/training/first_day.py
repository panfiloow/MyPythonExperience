"Умный кэширующий декоратор с TTL и ограничением памяти"

# Создайте декоратор @smart_cache с следующими возможностями:

# Время жизни кэша (TTL) в секундах

# Максимальное количество элементов в кэше

# При превышении лимита удаляются самые старые элементы (LRU)

# Кэширование по аргументам функции (учитывать позиционные и именованные)

# Возможность сбросить кэш для конкретной функции

# Пример использования
# @smart_cache(ttl=300, max_size=100)
# def expensive_operation(x, y=0):
#     # Тяжелые вычисления
#     return x * y + x ** 2

import time
from functools import wraps

def smart_cache(ttl=300, max_size=100):
    def decorator(func):
        cache = {}
        usage_order = []
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            
            if key in cache:
                cached_data = cache[key]
                if time.time() - cached_data['timestamp'] < ttl:
                    usage_order.remove(key)
                    usage_order.append(key)
                    return cached_data['result']
                else:
                    del cache[key]
                    usage_order.remove(key)
            
            result = func(*args, **kwargs)
            
            if len(cache) >= max_size:
                oldest_key = usage_order.pop(0)
                del cache[oldest_key]
            
            cache[key] = {
                'result': result,
                'timestamp': time.time()
            }
            usage_order.append(key)
            
            return result
        
        def make_key(args, kwargs):
            key = args
            if kwargs:
                key += tuple(sorted(kwargs.items()))
            return key
        
        def clear_cache():
            cache.clear()
            usage_order.clear()
        
        def get_stats():
            return {
                'hits': getattr(wrapper, '_hits', 0),
                'misses': getattr(wrapper, '_misses', 0),
                'size': len(cache),
                'hit_ratio': getattr(wrapper, '_hits', 0) / max(1, getattr(wrapper, '_hits', 0) + getattr(wrapper, '_misses', 0))
            }
        
        wrapper.clear_cache = clear_cache
        wrapper.get_stats = get_stats
        wrapper._hits = 0
        wrapper._misses = 0
        
        return wrapper
    return decorator

@smart_cache(ttl=300, max_size=50)
def expensive_operation(x, y=0):
    # Имитация тяжелых вычислений
    time.sleep(0.1)  
    return x * y + x ** 2

def test_performance():
    print("=== Тест производительности кэша ===")
    
    start_time = time.time()
    result1 = expensive_operation(5, 3)
    first_call_time = time.time() - start_time
    
    start_time = time.time()
    result2 = expensive_operation(5, 3)
    second_call_time = time.time() - start_time
    
    print(f"Первый вызов: {first_call_time:.4f} сек")
    print(f"Второй вызов: {second_call_time:.4f} сек")
    print(f"Ускорение: {first_call_time / second_call_time:.1f}x")
    print(f"Статистика: {expensive_operation.get_stats()}")

def test_multiple_calls():
    print("\n=== Тест с множественными вызовами ===")
    
    expensive_operation.clear_cache()
    
    test_cases = [(i, i % 3) for i in range(10)] * 3  
    
    start_time = time.time()
    
    for x, y in test_cases:
        expensive_operation(x, y)
    
    total_time = time.time() - start_time
    stats = expensive_operation.get_stats()
    
    print(f"Всего вызовов: {len(test_cases)}")
    print(f"Общее время: {total_time:.4f} сек")
    print(f"Статистика: {stats}")
    print(f"Экономия времени: {(1 - total_time / (len(test_cases) * 0.1)) * 100:.1f}%")

if __name__ == "__main__":
    test_performance()
    test_multiple_calls()

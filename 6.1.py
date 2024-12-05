def pipe(*funcs):
    # Проверяем, что все аргументы - функции
    if not all(callable(func) for func in funcs):
        raise TypeError("All arguments to pipe must be functions")

    # Возвращаем функцию-композицию
    def composed(x):
        result = x
        for func in funcs:
            result = func(result)
        return result

    return composed


# Пример использования:
inc = lambda x: x + 1
twice = lambda x: x * 2
cube = lambda x: x ** 3

# Создаем композицию функций
f = pipe(inc, twice, cube)

# Тестируем
x = f(5)  # Ожидаем: (((5 + 1) * 2) ** 3) = 1728
print(x)  # Вывод: 1728

# Пример с ошибкой:
try:
    f = pipe(inc, 7, cube)  # Это должно вызвать ошибку
except TypeError as e:
    print(e)  # Вывод: All arguments to pipe must be functions

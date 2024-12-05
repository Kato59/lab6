class SafePipe:
    def __init__(self, *funcs):
        if not all(callable(func) for func in funcs):
            raise TypeError("All arguments to SafePipe must be functions")
        self.funcs = funcs
        self.error_callbacks = []

    def __call__(self, x):
        result = x
        for func in reversed(self.funcs):  # Идем справа налево
            try:
                result = func(result)
            except Exception as e:
                result = None
                self._notify_error(e)
                break
        return result

    def on(self, event, callback):
        if event == 'error' and callable(callback):
            self.error_callbacks.append(callback)
        else:
            raise ValueError("Supported event is 'error' with a callable callback")

    def _notify_error(self, error):
        for callback in self.error_callbacks:
            callback(error)


# Пример использования
inc = lambda x: x + 1
twice = lambda x: x * 2
throw_error = lambda x: 1 / 0 if x == 5 else x ** 2

# Создаем безопасную композицию
f = SafePipe(inc, twice, throw_error)

# Подписка на ошибки
f.on('error', lambda e: print(f"Error caught: {e}"))

# Тестируем
result = f(5)  # Вызовет ошибку в throw_error
print(result)  # None

result = f(2)  # Работает без ошибок
print(result)  # (((2 ** 2) * 2) + 1) = 9

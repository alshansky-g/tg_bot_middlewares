import logging
import tracemalloc
import time
import functools
import types
import io

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

tracemalloc.start()

class LoggingMeta(type):
    def __new__(cls, name, bases, class_dict):
        for attr_name, attr_value in class_dict.items():
            if callable(attr_value) and not attr_name.startswith('__'):
                class_dict[attr_name] = cls._log_methods(attr_value, attr_name)
        return super().__new__(cls, name, bases, class_dict)


    def __call__(cls, *args, **kwargs):
        logger.info(f'Создание экземпляра класса: {cls.__name__}')
        instance = super().__call__(*args, **kwargs)
        instance.__call_stats__ = {}
        return instance

    @staticmethod
    def get_statistics(obj):
        logger.info('\nСтатистика вызовов методов:')
        for name, count in obj.__call_stats__.items():
            logger.info('%s - %s раз(а)', name, count)

    @staticmethod
    def _log_methods(method, method_name):
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            logger.info(f'Вызов метода: {method_name} объекта {self.__class__.__name__}')
            start = time.perf_counter()
            tracemalloc.start()
            mem_before, _ = tracemalloc.get_traced_memory()
            result = method(self, *args, **kwargs)
            mem_after, _ = tracemalloc.get_traced_memory()
            logger.info(f'Время выполнения метода {method_name}: {(time.perf_counter() - start) * 1000:.2f}  мс')
            logging.info(f'Использование памяти: до = {mem_before} байт, после = {mem_after} байт, разница = {mem_after - mem_before:+} байт')
            self.__call_stats__[method_name] = self.__call_stats__.get(method_name, 0) + 1
            return result
        return wrapper


class Worker:
    def __init__(self, name, surname, age, position, salary):
        self.name = name
        self.surname = surname
        self.age = age
        self.position = position
        self.salary = salary

    def __str__(self):
        return f"Работник {self.name} {self.surname}. Должность: {self.position}. Зарплата: {self.salary}"

    def salary_after_time(self, time):
        print(f'Ожидаемая зарплата: {self.salary * (time + 1)}')


gleb = Worker('Глеб', "Альшанский", 33, "разработчик", 100_000)
print(gleb)
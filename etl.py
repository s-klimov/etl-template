from collections.abc import Generator
from functools import wraps
from typing import Tuple, Dict, Any

import psycopg2
from psycopg2.extras import DictCursor, DictRow

SQL = """select id, number from etl.source"""


def coroutine(func):
    @wraps(func)
    def inner(*args:tuple[Any, ...], **kwargs: dict[str, Any]) -> Generator:
        fn: Generator = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def extract(batch: Generator) -> None:
    """ Извлекает из БД строки и передает их в генератор

    Args:
        batch: функция-генератор, в которую мы передаем значение

    """

    dbs: Dict = dict(dbname='demo', user='sergei', password='sergei', host='localhost')
    with psycopg2.connect(**dbs) as connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(SQL)
            record = cursor.fetchone()  # можно использовать fetchmany, чтобы извлекать данные "пачками"
            while record:
                batch.send(record)  # следим за тем, чтобы аргументом был итерируемый объект
                record = cursor.fetchone()


@coroutine
def transform(batch: Generator) -> Generator[None, DictRow, None]:

    foo: int | str  # инструкция для mypy

    while record := (yield):

        new_number = record["number"] ** 2
        if record["number"] % 2 == 0:
            foo = "an even number"
        elif record["number"] == 3:
            print("skip load stage")
            continue
        else:
            foo = 0

        batch.send((new_number, foo))


@coroutine
def load() -> Generator[None, Tuple, None]:
    while subject := (yield):
        match subject:
            case (int(number), str(bar)):
                print("the square of", bar, number)
            case (int(number), int(bar)):
                print(number)
            case _:
                raise SyntaxError(f"Unknown structure of {subject=}")

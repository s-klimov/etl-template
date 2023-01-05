from functools import wraps

import psycopg2
from psycopg2.extras import DictCursor


SQL = """select id, number from etl.source"""


def coroutine(func):
    @wraps(func)
    def inner(*args, **kwargs):
        fn = func(*args, **kwargs)
        next(fn)
        return fn

    return inner


def extract(batch):
    """ Извлекает из БД строки и передает их в генератор

    Args:
        batch: функция-генератор, в которую мы передаем значение

    """

    dbs = dict(dbname='demo', user='sergei', password='sergei', host='localhost')
    with psycopg2.connect(**dbs) as connection:
        with connection.cursor(cursor_factory=DictCursor) as cursor:
            cursor.execute(SQL)
            record = cursor.fetchone()  # можно использовать fetchmany, чтобы извлекать данные "пачками"
            while record:
                batch.send(record)  # следим за тем, чтобы аргументом был итерируемый объект
                record = cursor.fetchone()


@coroutine
def transform(batch):
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
def load():
    while subject := (yield):
        match subject:
            case (int(number), str(bar)):
                print("the square of", bar, number)
            case (int(number), int(bar)):
                print(number)
            case _:
                raise SyntaxError(f"Unknown structure of {subject=}")

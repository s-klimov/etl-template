from functools import wraps
from typing import Any, AsyncGenerator, Tuple

import anyio
import asyncpg
from anyio.abc import TaskGroup

SQL = """select id, number from etl.source"""


def coroutine(func):
    @wraps(func)
    async def inner(*args: tuple[Any, ...], **kwargs: dict[str, Any]) -> AsyncGenerator:
        fn: AsyncGenerator = func(*args, **kwargs)
        await anext(fn)
        return fn

    return inner


async def extract(batch: AsyncGenerator) -> None:
    """Извлекает из БД строки и передает их в генератор

    Args:
        batch: функция-генератор, в которую мы передаем значение

    """

    conn = await asyncpg.connect(
        database="demo", user="sergei", password="sergei", host="localhost"
    )

    stmt = await conn.prepare(SQL)
    async with conn.transaction():
        async for record in stmt.cursor():
            await batch.asend(
                record
            )  # следим за тем, чтобы аргументом был итерируемый объект

    await conn.close()


@coroutine
async def transform(batch: AsyncGenerator, task_group: TaskGroup) -> AsyncGenerator:
    async def process(record):
        await anyio.sleep(2)
        new_number = record["number"] ** 2
        if record["number"] % 2 == 0:
            foo = "an even number"
        elif record["number"] == 3:
            print("skip load stage")
            return
        else:
            foo = 0
        await batch.asend((new_number, foo))

    while record := (yield):
        print(record)
        task_group.start_soon(process, record)


@coroutine
async def load(task_group: TaskGroup) -> AsyncGenerator:
    await anyio.sleep(0)

    async def process(subject: Tuple) -> None:
        match subject:
            case (int(number), str(bar)):
                print("the square of", bar, number)
            case (int(number), int(bar)):
                print(number)
            case _:
                raise SyntaxError(f"Unknown structure of {subject=}")

    while subject := (yield):
        task_group.start_soon(process, subject)

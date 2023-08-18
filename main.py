from anyio import create_task_group, run

import etl


async def main():
    async with create_task_group() as tg:
        unloads = await etl.load(tg)
        multiplication = await etl.transform(unloads, tg)
        await etl.extract(multiplication)


if __name__ == "__main__":
    run(main)

from celery import shared_task

from etl_app import etl


@shared_task(name="Задача ETL")
def etl_task(*args, **kwargs):
    unloads = etl.load()
    multiplication = etl.transform(unloads)
    etl.extract(multiplication)

    return "my result data"  # здесь может быть более полезная информация

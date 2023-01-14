from celery import shared_task

from etl_app import etl


@shared_task(name="Задача ETL")
def etl_task():
    unloads = etl.load()
    multiplication = etl.transform(unloads)
    etl.extract(multiplication)


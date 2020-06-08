from __future__ import absolute_import
from celery import Celery
import make_tesla_table8
from datetime import timedelta

s_app = Celery('celery_on_tesla', backend='amqp://localhost//', broker='amqp://localhost//')

class CeleryConfig:
    CELERYBEAT_SCHEDULE = {
        'add-after-every-minute': {
        'task': 'celery_on_tesla.tesla_celery',
        'schedule': timedelta(minutes=1), # minutes/second/hour
        'args': ("boyoung.gratia.kim@gmail.com", "zerooneai01")
        }
    }
i_app = Celery('celery_on_tesla', backend='amqp://localhost//', broker='amqp://localhost//')
i_app.config_from_object(CeleryConfig)

@s_app.task
def start_tesla_celery(email, password):
    make_tesla_table8.make_tesla_table_with_celery(email, password, 1)

@i_app.task()
def insert_tesla_celery(email, password):
    make_tesla_table8.make_tesla_table_with_celery(email, password, 2)



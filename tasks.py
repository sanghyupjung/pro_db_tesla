from celery import Celery
import time

app = Celery('tasks', backend='rpc://', broker='amqp://localhost//')

@app.task
def reverse(string):
    time.sleep(10)
    return string[::-1]

@app.task
def add(x, y):
    time.sleep(10)
    return x + y
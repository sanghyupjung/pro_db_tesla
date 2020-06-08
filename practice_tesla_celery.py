from celery import Celery
import make_tesla_table6

#app = Celery('practice_tesla_celery', backend='rpc://', broker='amqp://localhost//')
app = Celery('practice_tesla_celery', backend='amqp://localhost//', broker='amqp://localhost//')

@app.task
def tesla_celery(email, password):
    make_tesla_table6.make_tesla_table_with_celery(email, password)
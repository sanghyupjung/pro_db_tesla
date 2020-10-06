### Tesla API
This project is for getting data about state of tesla vehicles through unofficial tesla api

### How it works
- access to unofficial tesla api with email and password of tesla
- get data about state of tesla vehicles every 1 minute
- load data in database for tesla

### tesla_before_celery.py
[tesla_before_celery.py](https://github.com/sanghyupjung/pro_db_tesla/blob/master/tesla_before_celery.py)
- a source code before applying celery

### tesla_after_celery.py
[tesla_after_celery.py](https://github.com/sanghyupjung/pro_db_tesla/blob/master/tesla_after_celery.py)
- a source code after applying celery

### Celery
[First Steps with Celery](http://docs.celeryproject.org/en/latest/getting-started/first-steps-with-celery.html#celerytut-broker)
1. install celery and rabbitmq
* pip install celery
* apt-get install rabbitmq-server
* service rabbitmq-server start
2. execute celery worker in foreground
* celery -A (project name) worker -B -l info
3. execute celery worker in background
* celery multi start 1 -A tesla -B -l info
* celery status
* celery multi stopwait 1 -A tesla -B -l info

### Test files
- celery_on_tesla.py
- execute_tesla_celery.py
- make_tesla_table.py
- make_tesla_table2.py
- make_tesla_table3.py
- make_tesla_table4.py
- make_tesla_table5.py
- make_tesla_table6.py
- make_tesla_table7.py
- make_tesla_table8.py
- make_tesla_table9.py
- make_tesla_table10.py
- practice_tesla_celery.py
- tasks.py

### Loaded result example (just for example)
- tesla_idle_1124037660.csv
- tesla_work_1124037660.csv

### Requirements
<table>
<tr>
  <td>requirements</td>
  <td>
    <img src="https://img.shields.io/badge/python-v3.6.9-brightgreen">
  </td>
</tr>
<tr>
  <td>python packages</td>
  <td>
    <img src="https://img.shields.io/badge/rauth-v0.7.3-orange">
    <img src="https://img.shields.io/badge/pprint-v0.1-orange">
    <img src="https://img.shields.io/badge/peewee-v3.10.0-orange">
    <img src="https://img.shields.io/badge/celery-v4.4.0-orange">
  </td>
</tr>


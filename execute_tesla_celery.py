#from practice_tesla_celery import *
from celery_on_tesla import *

'''
if __name__ == '__main__':
    result = tesla_celery.delay('boyoung.gratia.kim@gmail.com', 'zerooneai01')
    #result.status
'''

#tesla_celery.delay('boyoung.gratia.kim@gmail.com', 'zerooneai01')
#result = tesla_celery.delay('boyoung.gratia.kim@gmail.com', 'zerooneai01')
#result.status

while(1):
    print('1 : input your email and password')
    print('2 : insert your data')
    print('3 : check your status')
    print('4 : exit')
    x = int(input('enter the number : '))
    print()
    if x == 1:
        email = input('email : ')
        password = input('password : ')
        result = start_tesla_celery.delay(email, password)
    elif x == 2:
        email = input('email : ')
        password = input('password : ')
        result = insert_tesla_celery.delay(email, password)
    elif x == 3:
        print(result.status)
    elif x == 4:
        print('good bye')
        exit()
    else:
        print('try again')
    print()



from app import celery

@celery.task(name='add')
def add(x, y):
    print('Hello job add')
    result = x + y
    return result
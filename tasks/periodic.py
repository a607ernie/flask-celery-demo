from app import celery


@celery.task(name='printy')
def printy(a, b):
    """添加定時任務"""
    print('job printy')
    print(a + b)
    return a + b

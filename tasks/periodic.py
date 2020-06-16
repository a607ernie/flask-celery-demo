from app import celery


@celery.task(name='printy')
def printy(a, b):
    """通过配置文件添加定时任务"""
    print('job printy')
    print(a + b)
    return a + b

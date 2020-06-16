# import tasks
imports = (
    'tasks.add',
    'tasks.periodic'
    )

# #Timezone
enable_utc=False
timezone='Asia/Taipei'

# Broker and Backend
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

# schedules
from datetime import timedelta
from celery.schedules import crontab

beat_schedule = {
    'printy-run every 10 seconds': {
        'task': 'printy',
        'schedule': timedelta(seconds=10), #每分鐘執行一次
        'args': (8,2)
    }
}
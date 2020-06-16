from app import create_app,celery

app = create_app('default')
app.app_context().push()

from app.task import celery

'''执行后台耗时任务

# 启动worker进程：
celery -A task.celery worker -l info
'''
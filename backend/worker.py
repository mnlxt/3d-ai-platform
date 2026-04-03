from celery import Celery
from app.core.config import settings

# 创建 Celery 应用
celery_app = Celery(
    "3d-ai-platform",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

# 配置 Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Shanghai",
    enable_utc=True,
)

# 自动发现任务
celery_app.autodiscover_tasks()

if __name__ == "__main__":
    celery_app.start()

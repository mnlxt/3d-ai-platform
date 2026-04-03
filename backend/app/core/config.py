from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # 项目配置
    PROJECT_NAME: str = "3D AI Creation Platform"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"

    # 数据库配置 (这里的默认值会被 .env 文件中的值覆盖)
    MYSQL_HOST: str = "127.0.0.1"
    MYSQL_PORT: int = 3308 
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "3dai2026"
    MYSQL_DATABASE: str = "3d_ai_platform"

    # MongoDB配置
    MONGODB_URL: str = "mongodb://root:3dai2026@127.0.0.1:27017/admin"

    # MinIO配置
    MINIO_ENDPOINT: str = "127.0.0.1:9000"
    MINIO_ACCESS_KEY: str = "admin"
    MINIO_SECRET_KEY: str = "3dai2026"
    MINIO_SECURE: bool = False

    # AI服务配置
    STABLE_DIFFUSION_API_KEY: Optional[str] = None
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    DEFAULT_LLM_MODEL: str = "llama3"

    # 异步任务 Redis & Celery 配置 (解决报错的核心命脉)
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_BROKER_URL: str = "redis://127.0.0.1:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://127.0.0.1:6379/0"

    # Pydantic v2 配置：指定读取 .env 文件，并且忽略不认识的多余变量防止报错
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

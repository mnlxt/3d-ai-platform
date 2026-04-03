from minio import Minio
from app.core.config import settings

# 创建 MinIO 客户端
client = Minio(
    settings.MINIO_ENDPOINT,
    access_key=settings.MINIO_ACCESS_KEY,
    secret_key=settings.MINIO_SECRET_KEY,
    secure=settings.MINIO_SECURE
)

# 桶名称
bucket_name = "3d-ai-assets"

# 检查桶是否存在
if not client.bucket_exists(bucket_name):
    # 创建桶
    client.make_bucket(bucket_name)
    print(f"✅ 桶 {bucket_name} 创建成功！")
    
    # 设置桶权限为公共
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"AWS": ["*"]},
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{bucket_name}/*"]
            }
        ]
    }
    client.set_bucket_policy(bucket_name, str(policy))
    print(f"✅ 桶 {bucket_name} 权限设置为 Public！")
else:
    print(f"⚠️  桶 {bucket_name} 已经存在！")

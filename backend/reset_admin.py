from app.db.session import engine
from sqlalchemy import text
from app.core.security import get_password_hash

print("重置管理员密码...")

# 新密码
new_password = "admin123"
# 获取密码哈希
hashed_password = get_password_hash(new_password)

try:
    # 使用原始 SQL 语句来更新管理员密码
    with engine.connect() as connection:
        # 更新管理员密码
        connection.execute(
            text("UPDATE users SET hashed_password = :hashed_password WHERE role = 'admin' LIMIT 1"),
            {
                "hashed_password": hashed_password
            }
        )
        connection.commit()
        
        print("管理员密码已重置为:", new_password)
except Exception as e:
    print("错误:", e)

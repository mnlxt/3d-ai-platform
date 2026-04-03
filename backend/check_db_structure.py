from app.db.session import engine
from sqlalchemy import text

print("检查数据库表结构...")

try:
    # 使用原始 SQL 语句来查询表结构
    with engine.connect() as connection:
        # 查看 users 表的结构
        result = connection.execute(
            text("DESCRIBE users")
        )
        
        print("users 表结构:")
        for row in result:
            print(row)
        
        # 查看管理员信息
        result = connection.execute(
            text("SELECT * FROM users WHERE role = 'admin' LIMIT 1")
        )
        
        print("\n管理员信息:")
        admin = result.fetchone()
        if admin:
            print(admin)
        else:
            print("未找到管理员账号")
except Exception as e:
    print(f"错误: {e}")

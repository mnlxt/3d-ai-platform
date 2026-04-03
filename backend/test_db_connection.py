from app.db.session import engine
from sqlalchemy import text

print("测试数据库连接...")

try:
    # 尝试连接数据库
    with engine.connect() as connection:
        # 执行一个简单的SQL语句
        result = connection.execute(text("SELECT 1"))
        print(f"✅ 数据库连接成功！结果: {result.fetchone()}")
        
    print("数据库连接测试通过！")
except Exception as e:
    print(f"❌ 数据库连接失败: {e}")

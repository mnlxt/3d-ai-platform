import time
from app.db.session import engine

def check_mysql_ready():
    """检查 MySQL 是否真正 Up"""
    print("正在检查 MySQL 数据库连接...")
    
    max_attempts = 30
    attempt = 0
    
    while attempt < max_attempts:
        try:
            with engine.connect() as connection:
                # 执行一个简单的 SQL 语句
                connection.execute("SELECT 1")
                print("✅ MySQL 数据库连接成功！")
                return True
        except Exception as e:
            attempt += 1
            print(f"⏳ 尝试 {attempt}/{max_attempts}: MySQL 连接失败 - {e}")
            time.sleep(2)
    
    print("❌ MySQL 数据库连接失败，达到最大尝试次数")
    return False

if __name__ == "__main__":
    check_mysql_ready()

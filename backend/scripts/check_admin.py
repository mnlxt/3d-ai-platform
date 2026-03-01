import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.core.config import settings

def check_admin_user():
    connection = pymysql.connect(
        host=settings.MYSQL_HOST,
        port=settings.MYSQL_PORT,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        database=settings.MYSQL_DATABASE,
        charset='utf8mb4'
    )
    
    try:
        with connection.cursor() as cursor:
            print("=" * 60)
            print("检查管理员账号")
            print("=" * 60)
            
            # 查询所有用户
            cursor.execute("SELECT id, username, email, role, is_active FROM users")
            users = cursor.fetchall()
            
            print(f"\n📋 用户列表（共 {len(users)} 个）：")
            print("-" * 60)
            for user in users:
                print(f"ID: {user[0]}, 用户名: {user[1]}, 邮箱: {user[2]}, 角色: {user[3]}, 状态: {'活跃' if user[4] else '禁用'}")
            
            # 查询管理员用户
            cursor.execute("SELECT * FROM users WHERE role = 'admin'")
            admin_users = cursor.fetchall()
            
            print(f"\n👑 管理员用户（共 {len(admin_users)} 个）：")
            print("-" * 60)
            for admin in admin_users:
                print(f"ID: {admin[0]}, 用户名: {admin[1]}, 邮箱: {admin[2]}, 角色: {admin[6]}")
            
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ 查询失败: {e}")
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    check_admin_user()

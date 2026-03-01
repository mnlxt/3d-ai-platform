import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.core.config import settings
import bcrypt
from datetime import datetime

def create_admin_user():
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
            print("创建管理员账号")
            print("=" * 60)
            
            # 管理员账号信息
            admin_username = "admin"
            admin_email = "admin@3dai.com"
            admin_password = "admin123456"
            admin_role = "admin"
            
            # 检查是否已存在
            cursor.execute(
                "SELECT id FROM users WHERE username = %s OR email = %s",
                (admin_username, admin_email)
            )
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"\n⚠️  管理员账号已存在（ID: {existing_user[0]}）")
                choice = input("是否删除并重新创建？(y/n): ")
                if choice.lower() != 'y':
                    print("操作已取消")
                    return
                
                # 删除现有账号
                cursor.execute("DELETE FROM users WHERE id = %s", (existing_user[0],))
                print("✅ 已删除现有管理员账号")
            
            # 加密密码
            hashed_password = bcrypt.hashpw(
                admin_password.encode('utf-8'),
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # 插入管理员账号
            cursor.execute("""
                INSERT INTO users (
                    username, 
                    email, 
                    hashed_password, 
                    role, 
                    is_active, 
                    is_verified,
                    gender,
                    created_at,
                    updated_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                admin_username,
                admin_email,
                hashed_password,
                admin_role,
                True,
                True,
                'secret',
                datetime.utcnow(),
                datetime.utcnow()
            ))
            
            connection.commit()
            
            print("\n" + "=" * 60)
            print("🎉 管理员账号创建成功！")
            print("=" * 60)
            print(f"\n📧 邮箱: {admin_email}")
            print(f"👤 用户名: {admin_username}")
            print(f"🔑 密码: {admin_password}")
            print(f"🏷️  角色: {admin_role}")
            print("\n⚠️  请登录后立即修改密码！")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ 创建失败: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    create_admin_user()

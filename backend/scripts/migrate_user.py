import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pymysql
from app.core.config import settings

def migrate_user_table():
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
            print("检查并添加 gender 字段...")
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'gender'
            """, (settings.MYSQL_DATABASE,))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN gender ENUM('male', 'female', 'secret') NOT NULL DEFAULT 'secret' 
                    AFTER avatar_url
                """)
                print("✅ gender 字段添加成功")
            else:
                print("ℹ️ gender 字段已存在")
            
            print("检查并添加 bio 字段...")
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'users' AND COLUMN_NAME = 'bio'
            """, (settings.MYSQL_DATABASE,))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE users 
                    ADD COLUMN bio TEXT NULL 
                    AFTER gender
                """)
                print("✅ bio 字段添加成功")
            else:
                print("ℹ️ bio 字段已存在")
            
        connection.commit()
        print("\n🎉 用户表迁移完成！")
        
    except Exception as e:
        print(f"❌ 迁移失败: {e}")
        connection.rollback()
    finally:
        connection.close()

if __name__ == "__main__":
    migrate_user_table()

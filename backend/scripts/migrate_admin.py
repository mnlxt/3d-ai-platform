import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pymysql
from app.core.config import settings

def migrate_admin_tables():
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
            print("管理员功能数据库迁移")
            print("=" * 60)
            
            # 1. 创建 appeals 表
            print("\n1. 创建 appeals 表...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS appeals (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    user_id INT NOT NULL,
                    type ENUM('account', 'content', 'other') NOT NULL DEFAULT 'other',
                    title VARCHAR(200) NOT NULL,
                    description TEXT NOT NULL,
                    status ENUM('pending', 'processing', 'resolved', 'rejected') NOT NULL DEFAULT 'pending',
                    admin_response TEXT,
                    resolved_by INT,
                    resolved_at DATETIME,
                    attachments JSON,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_user_id (user_id),
                    INDEX idx_status (status),
                    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (resolved_by) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✅ appeals 表创建成功")
            
            # 2. 创建 content_reports 表
            print("\n2. 创建 content_reports 表...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS content_reports (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    reporter_id INT NOT NULL,
                    project_id INT NOT NULL,
                    reason VARCHAR(500) NOT NULL,
                    description TEXT,
                    status ENUM('pending', 'reviewed', 'dismissed') NOT NULL DEFAULT 'pending',
                    admin_notes TEXT,
                    action_taken ENUM('none', 'warning', 'removed', 'banned') NOT NULL DEFAULT 'none',
                    reviewed_by INT,
                    reviewed_at DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    INDEX idx_reporter_id (reporter_id),
                    INDEX idx_project_id (project_id),
                    INDEX idx_status (status),
                    FOREIGN KEY (reporter_id) REFERENCES users(id) ON DELETE CASCADE,
                    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE,
                    FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
            """)
            print("   ✅ content_reports 表创建成功")
            
            # 3. 检查并添加 projects 表的 is_public 字段
            print("\n3. 检查 projects 表字段...")
            cursor.execute("""
                SELECT COUNT(*) FROM information_schema.COLUMNS 
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'projects' AND COLUMN_NAME = 'is_public'
            """, (settings.MYSQL_DATABASE,))
            
            if cursor.fetchone()[0] == 0:
                cursor.execute("""
                    ALTER TABLE projects 
                    ADD COLUMN is_public BOOLEAN NOT NULL DEFAULT TRUE 
                    AFTER status
                """)
                print("   ✅ is_public 字段添加成功")
            else:
                print("   ℹ️ is_public 字段已存在")
            
            connection.commit()
            print("\n" + "=" * 60)
            print("🎉 管理员功能数据库迁移完成！")
            print("=" * 60)
            
    except Exception as e:
        print(f"\n❌ 迁移失败: {e}")
        connection.rollback()
        raise
    finally:
        connection.close()

if __name__ == "__main__":
    migrate_admin_tables()

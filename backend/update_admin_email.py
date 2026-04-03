from app.db.session import engine
from sqlalchemy import text

print("为管理员添加邮箱...")

try:
    # 使用原始 SQL 语句来更新管理员邮箱
    with engine.connect() as connection:
        # 首先查看当前管理员信息
        result = connection.execute(
            text("SELECT id, username, email, role FROM users WHERE role = 'admin' LIMIT 1")
        )
        admin = result.fetchone()
        
        if admin:
            print(f"当前管理员信息:")
            print(f"ID: {admin[0]}")
            print(f"用户名: {admin[1]}")
            print(f"邮箱: {admin[2]}")
            print(f"角色: {admin[3]}")
            
            # 如果管理员没有邮箱，添加邮箱
            if not admin[2]:
                connection.execute(
                    text("UPDATE users SET email = 'admin@example.com' WHERE role = 'admin' LIMIT 1")
                )
                connection.commit()
                print("\n✅ 已为管理员添加邮箱: admin@example.com")
            else:
                print(f"\n⚠️  管理员已经有邮箱: {admin[2]}")
        else:
            print("❌ 未找到管理员账号")
except Exception as e:
    print(f"错误: {e}")

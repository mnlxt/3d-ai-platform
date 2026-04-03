from app.db.session import engine
from sqlalchemy import text
from passlib.context import CryptContext

print("检查管理员账号信息...")

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    # 使用原始 SQL 语句来查询管理员信息
    with engine.connect() as connection:
        # 查看管理员信息
        result = connection.execute(
            text("SELECT id, username, email, password, role FROM users WHERE role = 'admin' LIMIT 1")
        )
        admin = result.fetchone()
        
        if admin:
            print(f"管理员信息:")
            print(f"ID: {admin[0]}")
            print(f"用户名: {admin[1]}")
            print(f"邮箱: {admin[2]}")
            print(f"角色: {admin[4]}")
            print(f"密码哈希: {admin[3]}")
            
            # 验证密码
            test_password = "admin123"
            is_valid = pwd_context.verify(test_password, admin[3])
            print(f"\n密码验证: {is_valid}")
            if is_valid:
                print("✅ 密码正确")
            else:
                print("❌ 密码错误")
        else:
            print("❌ 未找到管理员账号")
except Exception as e:
    print(f"错误: {e}")

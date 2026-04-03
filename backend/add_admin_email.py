from app.db.session import SessionLocal
from app.models.user import User

# 获取数据库会话
db = SessionLocal()

try:
    # 查找管理员账号
    admin = db.query(User).filter(User.role == "admin").first()
    
    if admin:
        print(f"当前管理员信息:")
        print(f"ID: {admin.id}")
        print(f"用户名: {admin.username}")
        print(f"邮箱: {admin.email}")
        print(f"角色: {admin.role}")
        
        # 如果管理员没有邮箱，添加邮箱
        if not admin.email:
            admin.email = "admin@example.com"
            db.commit()
            print("\n✅ 已为管理员添加邮箱: admin@example.com")
        else:
            print("\n⚠️  管理员已经有邮箱: {admin.email}")
    else:
        print("❌ 未找到管理员账号")
finally:
    db.close()

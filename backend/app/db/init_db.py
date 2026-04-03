from app.db.session import SessionLocal
from app.models.user import User
from app.core.security import get_password_hash

def init_initial_data():
    """初始化初始数据"""
    db = SessionLocal()
    try:
        # 检查管理员账号是否存在
        admin = db.query(User).filter(User.role == "admin").first()
        
        if not admin:
            # 创建管理员账号
            admin = User(
                username="admin",
                email="admin@3dai.com",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                is_active=True,
                is_verified=True
            )
            db.add(admin)
            db.commit()
            print("[OK] 初始管理员账号已创建")
        else:
            print("[INFO] 管理员账号已存在，跳过创建")
    except Exception as e:
        print(f"[ERROR] 初始化数据失败: {e}")
        db.rollback()
    finally:
        db.close()

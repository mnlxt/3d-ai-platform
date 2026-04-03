from app.db.session import engine

print("Testing database connection...")

try:
    # Test connection
    engine.connect()
    print("Database connection successful!")
except Exception as e:
    print("Database connection failed:", str(e))

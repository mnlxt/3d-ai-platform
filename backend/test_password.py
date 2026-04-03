from app.core.security import verify_password

# 测试密码验证
print("测试密码验证...")

# 从数据库中获取的密码哈希
hashed_password = "$2b$12$ST9/XGbIapTYgQy9gHHduuLV7Vjznq5IeI1i8lkrYfO41l2uNa.Ki"

# 测试密码
test_password = "admin123"

# 验证密码
is_valid = verify_password(test_password, hashed_password)

print(f"密码: {test_password}")
print(f"密码哈希: {hashed_password}")
print(f"验证结果: {is_valid}")

if is_valid:
    print("✅ 密码验证成功")
else:
    print("❌ 密码验证失败")

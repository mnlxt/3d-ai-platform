import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

print("=" * 60)
print("测试注册和个人信息填写完整流程")
print("=" * 60)

# 1. 注册新用户
print("\n1. 注册新用户...")
register_data = {
    "username": "newuser3",
    "email": "newuser2@example.com",
    "password": "123456"
}

response = requests.post(f"{BASE_URL}/auth/register", json=register_data)
if response.status_code == 201:
    print("✅ 注册成功")
else:
    print(f"❌ 注册失败: {response.status_code}")
    print(response.text)
    exit(1)

# 2. 登录
print("\n2. 登录...")
login_data = {
    "email": "newuser2@example.com",
    "password": "123456"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user = response.json()["user"]
    print(f"✅ 登录成功")
    print(f"   用户名: {user['username']}")
    print(f"   邮箱: {user['email']}")
else:
    print(f"❌ 登录失败: {response.status_code}")
    exit(1)

# 3. 获取用户信息（验证初始状态）
print("\n3. 获取用户信息（验证初始状态）...")
response = requests.get(f"{BASE_URL}/users/me", headers=headers)
if response.status_code == 200:
    user = response.json()
    print("✅ 获取成功")
    print(f"   用户名: {user['username']}")
    print(f"   邮箱: {user['email']}")
    print(f"   性别: {user.get('gender', '未设置')}")
    print(f"   手机号: {user.get('phone', '未设置')}")
    print(f"   个人签名: {user.get('bio', '未设置')}")
else:
    print(f"❌ 获取失败: {response.status_code}")

# 4. 完善个人信息（模拟ProfileSetupView）
print("\n4. 完善个人信息...")
profile_data = {
    "avatar_url": "https://example.com/avatar.jpg",
    "gender": "male",
    "phone": "13800138000",
    "bio": "这是一个新用户的个人签名，热爱3D创作！"
}

response = requests.put(f"{BASE_URL}/users/me", json=profile_data, headers=headers)
if response.status_code == 200:
    user = response.json()
    print("✅ 个人信息保存成功")
    print(f"   头像: {user['avatar_url']}")
    print(f"   性别: {user['gender']}")
    print(f"   手机号: {user['phone']}")
    print(f"   签名: {user['bio']}")
else:
    print(f"❌ 保存失败: {response.status_code}")
    print(response.text)

# 5. 验证最终数据
print("\n5. 验证最终数据...")
response = requests.get(f"{BASE_URL}/users/me", headers=headers)
if response.status_code == 200:
    user = response.json()
    print("✅ 最终用户信息:")
    print(f"   ID: {user['id']}")
    print(f"   用户名: {user['username']}")
    print(f"   邮箱: {user['email']}")
    print(f"   头像: {user['avatar_url']}")
    print(f"   性别: {user['gender']}")
    print(f"   手机号: {user['phone']}")
    print(f"   个人签名: {user['bio']}")
    print(f"   角色: {user['role']}")
else:
    print(f"❌ 验证失败: {response.status_code}")

# 6. 测试修改密码
print("\n6. 测试修改密码...")
password_data = {
    "old_password": "123456",
    "new_password": "newpassword123"
}

response = requests.put(f"{BASE_URL}/users/me/password", json=password_data, headers=headers)
if response.status_code == 200:
    print("✅ 密码修改成功")
else:
    print(f"❌ 密码修改失败: {response.status_code}")
    print(response.text)

# 7. 使用新密码登录验证
print("\n7. 使用新密码登录验证...")
login_data = {
    "email": "newuser2@example.com",
    "password": "newpassword123"
}

response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    print("✅ 新密码登录成功")
else:
    print(f"❌ 新密码登录失败: {response.status_code}")

print("\n" + "=" * 60)
print("注册和个人信息填写流程测试完成！")
print("=" * 60)

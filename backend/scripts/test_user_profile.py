import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

login_data = {
    "email": "test@example.com",
    "password": "123456"
}

print("=" * 50)
print("测试用户个人资料API")
print("=" * 50)

# 1. 登录
print("\n1. 用户登录...")
response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
if response.status_code == 200:
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print(f"✅ 登录成功")
else:
    print(f"❌ 登录失败: {response.status_code}")
    exit(1)

# 2. 获取当前用户信息
print("\n2. 获取当前用户信息...")
response = requests.get(f"{BASE_URL}/users/me", headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 获取成功")
    print(f"   用户名: {user['username']}")
    print(f"   邮箱: {user['email']}")
    print(f"   性别: {user.get('gender', '未设置')}")
    print(f"   个人签名: {user.get('bio', '未设置')}")
else:
    print(f"❌ 获取失败: {response.status_code}")

# 3. 更新性别
print("\n3. 更新性别...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "gender": "male"
}, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 性别更新成功: {user['gender']}")
else:
    print(f"❌ 性别更新失败: {response.status_code}")
    print(response.text)

# 4. 更新个人签名
print("\n4. 更新个人签名...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "bio": "这是一个测试用户的个人签名，热爱3D创作！"
}, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 个人签名更新成功")
    print(f"   签名: {user['bio']}")
else:
    print(f"❌ 个人签名更新失败: {response.status_code}")

# 5. 更新用户名
print("\n5. 更新用户名...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "username": "testuser_updated"
}, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 用户名更新成功: {user['username']}")
else:
    print(f"❌ 用户名更新失败: {response.status_code}")
    print(response.text)

# 6. 更新手机号
print("\n6. 更新手机号...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "phone": "13800138000"
}, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 手机号更新成功: {user['phone']}")
else:
    print(f"❌ 手机号更新失败: {response.status_code}")

# 7. 批量更新多个字段
print("\n7. 批量更新多个字段...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "username": "testuser",
    "gender": "secret",
    "bio": "3D创作爱好者 | AI艺术探索者",
    "phone": "13900139000"
}, headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 批量更新成功")
    print(f"   用户名: {user['username']}")
    print(f"   性别: {user['gender']}")
    print(f"   手机号: {user['phone']}")
    print(f"   签名: {user['bio']}")
else:
    print(f"❌ 批量更新失败: {response.status_code}")

# 8. 验证最终数据
print("\n8. 验证最终数据...")
response = requests.get(f"{BASE_URL}/users/me", headers=headers)
if response.status_code == 200:
    user = response.json()
    print(f"✅ 最终用户信息:")
    print(f"   ID: {user['id']}")
    print(f"   用户名: {user['username']}")
    print(f"   邮箱: {user['email']}")
    print(f"   手机号: {user['phone']}")
    print(f"   性别: {user['gender']}")
    print(f"   个人签名: {user['bio']}")
    print(f"   角色: {user['role']}")
else:
    print(f"❌ 验证失败: {response.status_code}")

# 9. 测试无效性别值
print("\n9. 测试无效性别值...")
response = requests.put(f"{BASE_URL}/users/me", json={
    "gender": "invalid"
}, headers=headers)
if response.status_code == 400:
    print(f"✅ 正确拒绝无效性别值")
else:
    print(f"⚠️ 未正确验证性别值: {response.status_code}")

print("\n" + "=" * 50)
print("用户个人资料API测试完成！")
print("=" * 50)

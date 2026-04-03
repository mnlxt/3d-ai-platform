import requests

# 测试 API 文档页面
print("=" * 60)
print("测试 FastAPI API 文档")
print("=" * 60)

try:
    response = requests.get("http://localhost:8000/docs", timeout=5)
    if response.status_code == 200:
        print("✅ API 文档页面可访问: http://localhost:8000/docs")
    else:
        print(f"⚠️ API 文档页面返回状态码: {response.status_code}")
except Exception as e:
    print(f"❌ API 文档页面访问失败: {e}")

# 测试健康检查接口
print("\n" + "=" * 60)
print("测试健康检查接口")
print("=" * 60)

try:
    response = requests.get("http://localhost:8000/", timeout=5)
    if response.status_code == 200:
        print(f"✅ 健康检查接口正常: {response.json()}")
    else:
        print(f"⚠️ 健康检查接口返回状态码: {response.status_code}")
except Exception as e:
    print(f"❌ 健康检查接口访问失败: {e}")

# 测试登录接口
print("\n" + "=" * 60)
print("测试登录接口 (POST /api/v1/login/access-token)")
print("=" * 60)

try:
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    response = requests.post(
        "http://localhost:8000/api/v1/login/access-token",
        data=login_data,
        timeout=5
    )
    if response.status_code == 200:
        result = response.json()
        print(f"✅ 登录成功！")
        print(f"   Token 类型: {result.get('token_type', 'N/A')}")
        print(f"   访问令牌: {result.get('access_token', 'N/A')[:50]}...")
    else:
        print(f"⚠️ 登录接口返回状态码: {response.status_code}")
        print(f"   响应内容: {response.text}")
except Exception as e:
    print(f"❌ 登录接口访问失败: {e}")

print("\n" + "=" * 60)
print("API 测试完成")
print("=" * 60)

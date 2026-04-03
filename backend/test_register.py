import requests

# 测试注册 API
print("Testing register API...")

url = "http://localhost:8000/api/v1/auth/register"

# 测试数据
test_data = {
    "username": "testuser2",
    "email": "test2@example.com",
    "password": "password123"
}

try:
    response = requests.post(url, json=test_data)
    print("Status code:", response.status_code)
    print("Response:", response.text)
    
    if response.status_code == 201:
        print("Register API test passed!")
    else:
        print("Register API test failed!")
except Exception as e:
    print("Error:", e)

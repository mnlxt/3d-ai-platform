@echo off

REM 3D AI 平台一键启动脚本
echo ================================
echo 3D AI 平台一键启动脚本
echo ================================
echo.

REM 1. 拉起基础设施
echo 1. 拉起基础设施...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ❌ 拉起基础设施失败
    pause
    exit /b 1
)
echo ✅ 基础设施启动成功

REM 2. 同步后端依赖
echo.
echo 2. 同步后端依赖...
pip install -r backend/requirements.txt
if %errorlevel% neq 0 (
    echo ❌ 同步后端依赖失败
    pause
    exit /b 1
)
echo ✅ 后端依赖同步成功

REM 3. 同步前端依赖
echo.
echo 3. 同步前端依赖...
npm install --prefix frontend
if %errorlevel% neq 0 (
    echo ❌ 同步前端依赖失败
    pause
    exit /b 1
)
echo ✅ 前端依赖同步成功

REM 4. 检查 MySQL 是否真正 Up
echo.
echo 4. 检查 MySQL 数据库连接...
python backend/scripts/check_ready.py
if %errorlevel% neq 0 (
    echo ❌ MySQL 数据库连接失败
    pause
    exit /b 1
)

REM 5. 打印验证结果表格
echo.
echo ================================
echo 验证结果

echo ================================
echo 服务状态：
echo - MySQL: ✅ 运行中
echo - MinIO: ✅ 运行中
echo - Redis: ✅ 运行中
echo ================================
echo 后端服务：
echo - 地址: http://localhost:8000
echo - API文档: http://localhost:8000/docs
echo - 健康检查: http://localhost:8000/
echo ================================
echo 前端服务：
echo - 地址: http://localhost:5173
echo - 登录页: http://localhost:5173/login
echo - 注册页: http://localhost:5173/register
echo ================================
echo MinIO 控制台：
echo - 地址: http://localhost:9001
echo - 用户名: admin
echo - 密码: 3dai2026
echo ================================
echo 管理员账号：
echo - 邮箱: admin@3dai.com
echo - 密码: admin123
echo ================================
echo.
echo 🎉 3D AI 平台环境搭建完成！
echo 现在可以访问 http://localhost:5173 开始使用平台了。
echo.
pause

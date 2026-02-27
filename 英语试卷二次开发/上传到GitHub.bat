@echo off
echo ======================================
echo   GitHub上传脚本
echo ======================================
echo.

echo 请先在GitHub上创建仓库，然后告诉我仓库地址
echo.
echo 或者你可以手动操作：
echo 1. 访问 https://github.com/new
echo 2. 创建新仓库(Public)
echo 3. 把下面的命令在Git Bash中运行
echo.

echo ======================================
echo 或者直接用这个命令（在Git Bash中运行）：
echo ======================================
echo.

echo git init
echo git add .
echo git commit -m "first commit"
echo git branch -M main
echo git remote add origin https://github.com/你的用户名/仓库名.git
echo git push -u origin main

pause

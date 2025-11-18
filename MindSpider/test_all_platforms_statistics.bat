@echo off
chcp 65001 >nul
set "PYTHONIOENCODING=utf-8"
REM 测试所有平台数据统计
echo ========================================
echo 测试所有平台数据统计
echo ========================================
echo.

REM 1. Activate conda environment
echo Activating conda environment...
call conda activate mindspider
if %errorlevel% neq 0 (
    echo Error: Cannot activate conda environment 'mindspider'
    echo Please create it first: conda create -n mindspider python=3.9
    pause
    exit /b 1
)
echo OK - Conda environment activated
echo.


echo 1. 查看所有平台汇总统计
python check_crawled_data.py
echo.

echo 2. 查看B站详细数据
python check_crawled_data.py --platform bili
echo.

echo 3. 查看微博详细数据
python check_crawled_data.py --platform weibo
echo.

echo 4. 查看小红书详细数据
python check_crawled_data.py --platform xhs
echo.

echo 5. 查看抖音详细数据
python check_crawled_data.py --platform douyin
echo.

echo 6. 查看快手详细数据
python check_crawled_data.py --platform kuaishou
echo.

echo 7. 查看贴吧详细数据
python check_crawled_data.py --platform tieba
echo.

echo 8. 查看知乎详细数据
python check_crawled_data.py --platform zhihu
echo.

echo ========================================
echo 测试完成！
echo ========================================
pause

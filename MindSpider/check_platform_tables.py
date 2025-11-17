# -*- coding: utf-8 -*-
"""检查数据库中的平台表"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import settings
import psycopg2

conn = psycopg2.connect(
    host=settings.DB_HOST,
    port=settings.DB_PORT,
    user=settings.DB_USER,
    password=settings.DB_PASSWORD,
    dbname=settings.DB_NAME,
)
cursor = conn.cursor()

# 查询所有表
cursor.execute(
    """
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    AND table_name LIKE '%video%' OR table_name LIKE '%note%' OR table_name LIKE '%aweme%'
    ORDER BY table_name
"""
)

tables = cursor.fetchall()
print("平台相关的表:")
for table in tables:
    table_name = table[0]
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  {table_name}: {count} 条记录")

cursor.close()
conn.close()

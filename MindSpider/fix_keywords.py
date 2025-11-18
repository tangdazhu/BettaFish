# -*- coding: utf-8 -*-
import psycopg2
import json

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    user="bettafish",
    password="bettafish_2024",
    database="bettafish",
)
cur = conn.cursor()

# 获取当前关键词
cur.execute("SELECT id, keywords FROM daily_topics WHERE extract_date = '2025-11-17'")
result = cur.fetchone()
topic_id, keywords_json = result
keywords = json.loads(keywords_json)

print("Original keywords:")
for i, kw in enumerate(keywords, 1):
    print(f"  {i}. {repr(kw)}")

# 修复：去掉所有类型的引号
fixed_keywords = []
for kw in keywords:
    # 去掉各种引号: " " ' ' " ' 以及Unicode引号
    fixed = kw.replace('"', "").replace('"', "").replace('"', "")
    fixed = fixed.replace("'", "").replace("'", "").replace("'", "")
    fixed = fixed.replace("\u201c", "").replace("\u201d", "")  # Unicode左右双引号
    fixed = fixed.replace("\u2018", "").replace("\u2019", "")  # Unicode左右单引号
    fixed_keywords.append(fixed)

print("\nFixed keywords:")
for i, kw in enumerate(fixed_keywords, 1):
    print(f"  {i}. {repr(kw)}")

# 更新数据库
fixed_json = json.dumps(fixed_keywords, ensure_ascii=False)
cur.execute(
    "UPDATE daily_topics SET keywords = %s WHERE id = %s", (fixed_json, topic_id)
)
conn.commit()

print("\n[OK] Database updated!")

cur.close()
conn.close()

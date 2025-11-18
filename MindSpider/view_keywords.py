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
cur.execute("SELECT keywords FROM daily_topics WHERE extract_date = '2025-11-17'")
result = cur.fetchone()
keywords = json.loads(result[0])
print("Keywords:", keywords)
for i, kw in enumerate(keywords):
    print(f"{i+1}. repr: {repr(kw)}")
    print(f'   bytes: {kw.encode("utf-8")}')
cur.close()
conn.close()

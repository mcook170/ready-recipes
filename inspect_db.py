import sqlite3
conn = sqlite3.connect("recipes.db")
cur = conn.cursor()
cur.execute("PRAGMA table_info(recipes)")
print(cur.fetchall())
conn.close()
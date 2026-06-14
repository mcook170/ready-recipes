import sqlite3

conn = sqlite3.connect("recipesA.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(recipes);")
columns = cursor.fetchall()

for col in columns:
    print(col)

conn.close()

import sqlite3

# CHANGE THIS to your actual database filename
db_path = "recipes.db"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Add new columns
cursor.execute("ALTER TABLE recipes ADD COLUMN ingredients TEXT;")
cursor.execute("ALTER TABLE recipes ADD COLUMN instructions TEXT;")

conn.commit()
conn.close()

print("Database updated successfully!")

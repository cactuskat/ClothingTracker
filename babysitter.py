import sqlite3

conn = sqlite3.connect("closet_list.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

cursor.execute("SELECT * FROM closet;")
rows = cursor.fetchall()
for row in rows:
    print(row)

conn.close()

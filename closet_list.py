import sqlite3

connection = sqlite3.connect("closet_list.db")
cursor = connection.cursor()

cursor.execute("CREATE TABLE IF NOT EXISTS closet (" \
    "id INTEGER PRIMARY KEY AUTOINCREMENT," \
    "name TEXT NOT NULL," \
    "type TEXT NOT NULL," \
    "weather TEXT NOT NULL," \
    "img_path TEXT NOT NULL)");

cursor.execute("INSERT INTO closet (name,type,weather,img_path) VALUES (?,?,?,?)",
               ('Shirt1','top','hot','imgs/Tops/shirt1.png')
               )
cursor.execute("INSERT INTO closet (name,type,weather,img_path) VALUES (?,?,?,?)",
               ('Pants1','bottom','hot','imgs/Bottoms/pants1.png')
               )

connection.commit()
connection.close()
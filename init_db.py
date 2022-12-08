import sqlite3

connection = sqlite3.connect("db.sqlite3")

with open("init.sql") as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute(
    "INSERT INTO users (id, email, password) VALUES (?, ?, ?)",
    (1, "aderibigbeganiu@gmail.com", "Adeganew1"),
)


connection.commit()
connection.close()

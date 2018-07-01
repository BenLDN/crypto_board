import sqlite3
import hashlib

conn = sqlite3.connect('users.db')
print("Opened database successfully")

conn.execute('CREATE TABLE usr (usr_name TEXT, reg_date TEXT, pw_hash, cash INT, btc INT)')
print("Table created successfully")
conn.execute("insert into usr values(?, ?, ?, ?, ?)", ("admin", "plchldr", hashlib.sha256("123".encode()).hexdigest(), 100000, 0))
conn.execute("insert into usr values(?, ?, ?, ?, ?)", ("test", "plchldr", hashlib.sha256("456".encode()).hexdigest(), 50000, 5))
conn.commit()
conn.close()

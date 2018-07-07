#This script creates the DB for users, it's not needed after that

import sqlite3
import hashlib

conn = sqlite3.connect('users.db')
print("Opened database successfully")

conn.execute('CREATE TABLE usr (user_name TEXT, registration_date TEXT, password_hash, total_cash INT, total_btc INT)')
print("Table created successfully")
conn.execute("insert into usr values(?, ?, ?, ?, ?)", ("admin", "plchldr", hashlib.sha256("123".encode()).hexdigest(), 100000, 0))
conn.execute("insert into usr values(?, ?, ?, ?, ?)", ("test", "plchldr", hashlib.sha256("456".encode()).hexdigest(), 100000, 0))
conn.commit()
conn.close()

import sqlite3
import hashlib

conn = sqlite3.connect('users.db')
print("Opened database successfully")

conn.execute('CREATE TABLE usr (usr_name TEXT, reg_date TEXT, pw_hash)')
print("Table created successfully")
conn.execute("insert into usr values(?, ?, ?)", ("admin".upper(), "plchldr", hashlib.sha256("123".encode()).hexdigest()))
conn.execute("insert into usr values(?, ?, ?)", ("test".upper(), "plchldr", hashlib.sha256("456".encode()).hexdigest()))
conn.commit()
conn.close()

import sqlite3

conn = sqlite3.connect('messages.db')
print("Opened database successfully")

conn.execute('CREATE TABLE msg (name TEXT, msg_date TEXT, price INT, msg_content TEXT, buy_amount INT, new_cash INT, new_btc INT)')
print("Table created successfully")
conn.close()
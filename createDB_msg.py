import sqlite3

conn = sqlite3.connect('messages.db')
print("Opened database successfully")

conn.execute('CREATE TABLE msg (user_name TEXT, message_date TEXT, btc_price INT, message_content TEXT, transaction_amount INT, new_cash INT, new_btc INT, net_worth INT)')
print("Table created successfully")
conn.close()
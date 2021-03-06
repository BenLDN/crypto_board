#Database functions used by crypto_board.py

import sqlite3 as sql
import hashlib
import datetime

db_path=""

#list users -> used to check if the user name entered at login exists
def list_users():
	conn = sql.connect(db_path+'users.db')
	c = conn.cursor()
	c.execute("select user_name from usr;")
	result = [x[0] for x in c.fetchall()]
	conn.close()
	return result

#compare a password's hash to the one stored in the DB -> used to check the password at login
def verify_login(user_name_check, password_check):
    conn = sql.connect('users.db')
    c = conn.cursor()
    c.execute("select password_hash from usr where user_name = '" + user_name_check + "';")
    result = c.fetchone()[0] == hashlib.sha256(password_check.encode()).hexdigest()
    conn.close()
    return result

#delete all messages and reset balances -> only the admin can do this
def clear_and_reset():
	#delete messages
	con = sql.connect(db_path+"messages.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("delete from msg")
	con.commit()
	con.close()

	#reset balances to usd 100k and btc 0
	# con = sql.connect('users.db')
	# con.execute("update usr set total_cash = 100000")
	# con.execute("update usr set total_btc = 0")
	# con.commit()
	# con.close()
	set_usd_and_btc("*", 0, 100000)

#get all messages to be listed as part of the main page (in reverse order to show the newest at the top)
def list_messages():
   con = sql.connect(db_path+"messages.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select rowid, * from msg")
   rows = cur.fetchall()
   con.close()
   rows.reverse()
   return rows

#updating the user's btc and dollar balance -> used when a message with a transaction is submitted
def update_user(current_user, transaction_type, transaction_amount, btc_price):
	
	#reading current btc & dollar amounts
	old_cash, old_btc = get_usd_and_btc(current_user)
	
	#calculating the new btc & dollar amounts after the transaction
	if transaction_type == "buy":
		new_cash=old_cash-(btc_price*transaction_amount)
		new_btc=old_btc+transaction_amount
	else:
		transaction_amount*=-1
		new_cash=old_cash-btc_price*transaction_amount
		new_btc=old_btc+transaction_amount

	#error check: if the transaction would result in a negative cash or btc value -> return -1,0 or 0,-1 and don't change anything in the DB
	if new_cash < 0:
		return -1, 0
	if new_btc < 0:
		return 0, -1

	#updating the btc & dollar amounts in the DB, returning the new values (as they are needed to post the message)
	set_usd_and_btc(current_user, new_btc, new_cash)

	return new_cash, new_btc

#add the message to the DB -> used when a message with a transaction is submitted
def post_message(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth):
	con = sql.connect(db_path+"messages.db")
	cur = con.cursor()
	net_worth=new_cash+btc_price*new_btc
	cur.execute("INSERT INTO msg (user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth) VALUES (?,?,?,?,?,?,?,?)",(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth))
	con.commit()
	con.close()

#get the user's btc and usd balances
def get_usd_and_btc(current_user):
	con = sql.connect(db_path+"users.db")
	cur = con.cursor()
	cur.execute("SELECT total_cash, total_btc from usr WHERE user_name=?", (current_user,))
	total_cash, total_btc = cur.fetchall()[0]
	return total_cash, total_btc

#set the user's btc and usd balances
def set_usd_and_btc(current_user, new_btc, new_cash):
	con = sql.connect(db_path+"users.db")
	cur = con.cursor()
	cur.execute("UPDATE usr SET total_cash=?, total_btc=? WHERE user_name=?", (new_cash, new_btc, current_user,))
	con.commit()
	con.close()

def register_user(user_name, user_password):
	conn = sql.connect(db_path+'users.db')
	conn.execute("insert into usr values(?, ?, ?, ?, ?)", (user_name, "plchldr", hashlib.sha256(user_password.encode()).hexdigest(), 100000, 0))
	conn.commit()
	conn.close()
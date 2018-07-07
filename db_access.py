#Database functions used by crypto_board.py

import sqlite3 as sql
import hashlib
import datetime

#list users -> used to check if the user name entered at login exists
def list_users():
	conn = sql.connect('users.db')
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
	con = sql.connect("messages.db")
	con.row_factory = sql.Row
	cur = con.cursor()
	cur.execute("delete from msg")
	con.commit()
	con.close()

	#reset balances to usd 100k and btc 0
	

#get all messages to be listed as part of the main page (in reverse order to show the newest at the top)
def list_messages():
   con = sql.connect("messages.db")
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
	con = sql.connect("users.db")
	cur = con.cursor()
	cur.execute("SELECT total_cash, total_btc from usr WHERE user_name=?", (current_user,))
	old_cash, old_btc = cur.fetchall()[0]
	
	#calculating the new btc & dollar amounts after the transaction
	if transaction_type == "buy":
		new_cash=old_cash-(btc_price*transaction_amount)
		new_btc=old_btc+transaction_amount
	else:
		transaction_amount*=-1
		new_cash=old_cash-btc_price*transaction_amount
		new_btc=old_btc+transaction_amount

	#updating the btc & dollar amounts in the DB, returning the new values (as they are needed to post the message)
	cur.execute("UPDATE usr SET total_cash=?, total_btc=? WHERE user_name=?", (new_cash, new_btc, current_user,))
	con.commit()
	con.close()
	return new_cash, new_btc

#add the message to the DB -> used when a message with a transaction is submitted
def post_message(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth):
	con = sql.connect("messages.db")
	cur = con.cursor()
	net_worth=new_cash+btc_price*new_btc
	cur.execute("INSERT INTO msg (user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth) VALUES (?,?,?,?,?,?,?,?)",(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth))
	con.commit()
	con.close()
#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, session
from werkzeug.contrib.cache import SimpleCache
import sqlite3 as sql
import get_btc_price
import hashlib
import datetime

def list_users():
    conn = sql.connect('users.db')
    c = conn.cursor()

    c.execute("select user_name from usr;")
    result = [x[0] for x in c.fetchall()]

    conn.close()
    
    return result

def verify_login(user_name_check, password_check):
    conn = sql.connect('users.db')
    c = conn.cursor()

    c.execute("select password_hash from usr where user_name = '" + user_name_check + "';")
    result = c.fetchone()[0] == hashlib.sha256(password_check.encode()).hexdigest()
    
    conn.close()

    return result

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')

def list_messages():
   con = sql.connect("messages.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select rowid, * from msg")
   
   rows = cur.fetchall()
   con.close()

   rows.reverse()

   return render_template("index.html",rows = rows)

@app.route('/login', methods = ['POST'])
def login():
	user_name = request.form.get('user_name')
	if (user_name in list_users()) and verify_login(user_name, request.form.get('user_password')):
		session['current_user'] = user_name
    
	return(redirect('/'))

@app.route("/logout/")
def logout():
    session.pop("current_user", None)
    return(redirect('/'))

#not used directly, the form in index.html posts data to /new_msg
@app.route('/new_msg', methods = ['POST'])
def new_msg():
	if request.method == "POST":
		
		user_name = session.get("current_user")
		message_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		message_content = request.form['message_content']

		btc_price = cache.get('btc_cached_price')
		   
		if btc_price is None:
			btc_price = get_btc_price.get_btc_price()
			cache.set('btc_cached_price', btc_price, timeout = 60)

		new_cash=10
		new_btc=10

		con = sql.connect("users.db")
		cur = con.cursor()

		cur.execute("SELECT total_cash, total_btc from usr WHERE user_name=?", (session['current_user'],))

		old_cash, old_btc = cur.fetchall()[0]
		
		if request.form['transaction_type'] == "buy":
			transaction_amount=int(request.form['transaction_amount'])
			new_cash=old_cash-(btc_price*transaction_amount)
			new_btc=old_btc+transaction_amount
		else:
			transaction_amount=-int(request.form['transaction_amount'])
			new_cash=old_cash-btc_price*transaction_amount
			new_btc=old_btc+transaction_amount

		cur.execute("UPDATE usr SET total_cash=?, total_btc=? WHERE user_name=?", (new_cash, new_btc, session['current_user']))
        
		con.commit()
  
		con.close()
		
     
		con = sql.connect("messages.db")
		cur = con.cursor()

		net_worth=new_cash+btc_price*new_btc

		cur.execute("INSERT INTO msg (user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth) VALUES (?,?,?,?,?,?,?,?)",(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth))
        
		con.commit()
  
		con.close()

	return redirect('/')

@app.route('/clear')
def clear():
	con = sql.connect("messages.db")
	con.row_factory = sql.Row
   
	cur = con.cursor()
	cur.execute("delete from msg")
	con.commit()

	con.close()
	return redirect('/')

@app.route('/del_msg')
def del_msg():
	pass

if __name__ == '__main__':
	cache = SimpleCache()
	app.run(host='0.0.0.0', debug = True)
#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
import get_prices
import db_access
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def main_page():
   
   messages=db_access.list_messages()

   return render_template("index.html",rows = messages)

@app.route('/login', methods = ['POST'])
def login():
	user_name = request.form.get('user_name')
	if (user_name in db_access.list_users()) and db_access.verify_login(user_name, request.form.get('user_password')):
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
		transaction_amount=int(request.form['transaction_amount'])
		transaction_type=request.form['transaction_type']

		btc_price = get_prices.get_btc_price()

		new_cash, new_btc = db_access.update_user(session['current_user'], transaction_type, transaction_amount, btc_price)	

		net_worth=new_cash+new_btc*btc_price
     	
		db_access.post_message(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth)


	return redirect('/')

@app.route('/clear')
def clear():
	db_access.clear_message_db()
	return redirect('/')

@app.route('/del_msg')
def del_msg():
	pass

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)
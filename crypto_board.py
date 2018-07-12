#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, session, flash
from flask_paginate import Pagination, get_page_parameter
import sqlite3 as sql
import get_prices
import db_access
import hashlib
import datetime

app = Flask(__name__)
app.secret_key = 'super secret key'

#main page = index.html template populated by the list of messages
@app.route('/')
def main_page():
	page = request.args.get(get_page_parameter(), type=int, default=1)
	per_page=3
	messages=db_access.list_messages()
	total = len(messages)
	pagination = Pagination(page=page, per_page=per_page, total=total)
	paginated_messages = messages[(page-1)*per_page:page*per_page]

	total_btc=total_cash=0
	
	if "current_user" in session:
		total_cash, total_btc = db_access.get_usd_and_btc(session.get("current_user"))
	
	return render_template("index.html",rows = paginated_messages, pagination=pagination, page=page, per_page=per_page, total_btc=total_btc, total_cash=total_cash)

#redirects to the main page after login
@app.route('/login', methods = ['POST'])
def login():
	
	user_name = request.form.get('user_name')
	user_password = request.form.get('user_password')	

	#if the Log In button was press -> login & redirect to main page
	if request.form.get('action') == "login":
		if (user_name in db_access.list_users()) and db_access.verify_login(user_name, user_password):
			session['current_user'] = user_name 
		return(redirect('/'))

	#if the Sign Up button was press -> register user & redirect to main page
	if request.form.get('action') == "signup":
		db_access.register_user(user_name, user_password)
	
	return(redirect('/'))

#redirects to the main page after logout
@app.route("/logout/")
def logout():
    session.pop("current_user", None)
    return(redirect('/'))

#redirects to the main page after updating the user's money and btc in the database and posting the message
@app.route('/new_msg', methods = ['POST'])
def new_msg():

	#reading data from the form
	user_name = session.get("current_user")
	message_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	message_content = request.form['message_content']
	transaction_amount=int(request.form['transaction_amount'])
	transaction_type=request.form['transaction_type']

	#get the current price
	btc_price = get_prices.get_btc_price()

	#updating the user's dollar and btc balance and returning the new balances
	new_cash, new_btc = db_access.update_user(session['current_user'], transaction_type, transaction_amount, btc_price)	

 	#posting the message - we need the updated btc and dollar balance#
	if transaction_type == "sell":
 		transaction_amount*=-1
	net_worth=new_cash+new_btc*btc_price
	db_access.post_message(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth)

	return redirect('/')

#redirects to the main page after deleting all messages and reseting usd & btc balances (only the admin can do this)
@app.route('/clear_and_reset')
def clear_and_reset():
	db_access.clear_and_reset()
	return redirect('/')

if __name__ == '__main__':
	app.run(host='0.0.0.0', debug = True)
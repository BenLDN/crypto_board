#!/usr/bin/env python3

from flask import Flask, render_template, request, redirect, session
from werkzeug.contrib.cache import SimpleCache
import sqlite3 as sql
import get_time_btc_price
import hashlib
import datetime

def list_users():
    conn = sql.connect('users.db')
    c = conn.cursor()

    c.execute("select usr_name from usr;")
    result = [x[0] for x in c.fetchall()]

    conn.close()
    
    return result

def verify(usr_name_check, pw_check):
    conn = sql.connect('users.db')
    c = conn.cursor()

    c.execute("select pw_hash from usr where usr_name = '" + usr_name_check + "';")
    result = c.fetchone()[0] == hashlib.sha256(pw_check.encode()).hexdigest()
    
    conn.close()

    return result

app = Flask(__name__)
app.secret_key = 'super secret key'

@app.route('/')
def list():
   con = sql.connect("messages.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select rowid, * from msg")
   
   rows = cur.fetchall();
   con.close()

   rows.reverse()

   return render_template("index.html",rows = rows)

@app.route('/login', methods = ['POST'])
def login():
	usr_name = request.form.get('usr_name')
	if (usr_name in list_users()) and verify(usr_name, request.form.get('usr_pw')):
		session['current_user'] = usr_name
    
	return(redirect('/'))

@app.route("/logout/")
def logout():
    session.pop("current_user", None)
    return(redirect('/'))

#not used directly, the form in index.html posts data to /new_msg
@app.route('/new_msg', methods = ['POST'])
def new_msg():
	if request.method == "POST":
		
		name = session.get("current_user")
		msg_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		msg_content = request.form['msg_content']

		price = cache.get('btc')
		   
		if price is None:
			price = get_time_btc_price.get_btc_price()
			cache.set('btc', price, timeout = 60)
			msg_content+="not cached"
			
		
		
     
		con = sql.connect("messages.db")
		cur = con.cursor()
		cur.execute("INSERT INTO msg (name, msg_date, price, msg_content) VALUES (?,?,?,?)",(name, msg_date, price, msg_content))
        
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
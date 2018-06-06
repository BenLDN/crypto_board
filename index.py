#!/usr/bin/python3

from flask import Flask, render_template, request, redirect
import sqlite3 as sql
import get_time_btc_price

app = Flask(__name__)

@app.route('/')
def list():
   con = sql.connect("messages.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from msg")
   
   rows = cur.fetchall();
   con.close()

   rows.reverse()

   return render_template("index.html",rows = rows)

#not used directly, the form in index.html posts data to /new_msg
@app.route('/new_msg', methods = ['POST'])
def new_msg():
	if request.method == "POST":
		
		name = request.form['name']
		msg_date, price = get_time_btc_price.get_time_btc_price()
		msg_content = request.form['msg_content']
     
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

if __name__ == '__main__':
   app.run(host='0.0.0.0', debug = True)

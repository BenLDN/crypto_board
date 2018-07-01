#!/usr/bin/env python3

#from flask import Flask, render_template, request, redirect, session
import sqlite3 as sql
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

def clear_message_db():
	con = sql.connect("messages.db")
	con.row_factory = sql.Row
   
	cur = con.cursor()
	cur.execute("delete from msg")
	con.commit()

	con.close()

def list_messages():
   con = sql.connect("messages.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select rowid, * from msg")
   
   rows = cur.fetchall()
   con.close()

   rows.reverse()

   return rows

def update_user(current_user, transaction_type, transaction_amount, btc_price):
	con = sql.connect("users.db")
	cur = con.cursor()

	cur.execute("SELECT total_cash, total_btc from usr WHERE user_name=?", (current_user,))

	old_cash, old_btc = cur.fetchall()[0]
	
	if transaction_type == "buy":
		new_cash=old_cash-(btc_price*transaction_amount)
		new_btc=old_btc+transaction_amount
	else:
		transaction_amount*=-1
		new_cash=old_cash-btc_price*transaction_amount
		new_btc=old_btc+transaction_amount

	cur.execute("UPDATE usr SET total_cash=?, total_btc=? WHERE user_name=?", (new_cash, new_btc, current_user,))
    
	con.commit()

	con.close()
	return new_cash, new_btc


def post_message(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth):
	con = sql.connect("messages.db")
	cur = con.cursor()

	net_worth=new_cash+btc_price*new_btc

	cur.execute("INSERT INTO msg (user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth) VALUES (?,?,?,?,?,?,?,?)",(user_name, message_date, btc_price, message_content, transaction_amount, new_cash, new_btc, net_worth))
    
	con.commit()

	con.close()
import json 
import requests
import datetime
import time
import sqlite3 as sql

def get_time_btc_price():

	r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')

	req_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	price_float = float(r.json()[0]["price_usd"])
	price=int(round(price_float))

	return req_time, price

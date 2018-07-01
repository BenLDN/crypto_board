import json 
import requests
import sqlite3 as sql


def get_btc_price():

	r = requests.get('https://api.coinmarketcap.com/v1/ticker/bitcoin/')

	price_float = float(r.json()[0]["price_usd"])
	price=int(round(price_float))

	return price

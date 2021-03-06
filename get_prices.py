import json 
import requests
import sqlite3 as sql
from werkzeug.contrib.cache import SimpleCache

cache = SimpleCache()


def get_btc_price_API():

	r = requests.get('https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD&e=Coinbase')

	price_float = float(r.json()['USD'])
	price=int(round(price_float))

	return price


def get_btc_price():
	
	btc_price = cache.get('btc_cached_price')

	#cache miss: call the API
	if btc_price is None:

		btc_price = get_btc_price_API()
		cache.set('btc_cached_price', btc_price, timeout = 60)

		new_cash=10
		new_btc=10

	return btc_price


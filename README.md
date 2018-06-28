# crypto_board
Simple message board that attaches the actual BTC price to each message.

Uses port 5000.

createDB.py: not part of the app, it was used to create the SQLite database (messages.db)

Tested on AWS EC2.

# Plan to improve the site

Add option to "bet" with virtual money:
	1 add money & btc for each user in DB
	2 add money & btc for each message in DB
	3 message list: show current money & btc of user
	4 message list: show transaction performed
	5 when posting message: buy/sell button
Add registration option
Add another board for ETH
Make it pretty & multiline comments

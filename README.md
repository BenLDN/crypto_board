# crypto_board
Simple message board that attaches the actual BTC price to each message.

Uses port 5000.

createDB.py: not part of the app, it was used to create the SQLite database (messages.db)

Tested on AWS EC2.

# Plan to improve the site

Add option to "bet" with virtual money:
	1 add money for each user to DB
	2 message list: show current money of user
	3 message list: show transaction performed
	4 when posting message: buy/sell button
Add registration option
Add another board for ETH
Make it pretty & multiline comments



python -i My_discord.py

scp -r /Users/matthieu/Documents/Python/Binance/Crypto_arbitrage_bot matthieu@192.168.1.19:/home/matthieu/python/Binance/

python -m pip install discord
python -m pip install python-kucoin
python -m pip install python-dotenv
python -m pip install tqdm
python -m pip install nest-asyncio

lxterminal -e "cd /home/matthieu/python/Binance/220605_Arbitrage/ ; python Main_Arbitrage.py"

source : https://medium.com/geekculture/automated-triangular-arbitrage-of-cryptos-in-4-steps-a678f7b01ce7

220605  - first version

220702	- add kucoin exchange

git help
git rm .env --cached
git commit -a -m "Stopped tracking .env File"
git push -u origin main
git filter-branch --index-filter "git rm -rf --cached --ignore-unmatch .env"  --> push --force ensuite https://stackoverflow.com/questions/54750229/remove-virtualenv-files-from-all-previous-commits-after-removing-from-repository
git pull --allow-unrelated-histories origin main  forcer le pull d un code local
git rev-parse --abbrev-ref HEAD

https://gist.github.com/KedrikG/f7b955dc371b1204ec76ce862e2dcd2e token et sublime text
https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github
https://github.com/Kunena/Kunena-Forum/wiki/Create-a-new-branch-with-git-and-manage-branches

https://stackoverflow.com/questions/68717924/correct-way-to-call-run-in-executor-for-blocking-code-in-asyncio-loop


2022-09-17 16:29:37,468 - kucoin PROFIT-16:29:37:BUY_SELL_SELL, PEEL-USDT,PEEL-BTC,BTC-USDT, Profit/Loss: 6.749PEEL-USDT: 0.114, PEEL-BTC: 7.002e-06, BTC-USDT: 19944.0
2022-09-17 16:29:37,468 - do_arbitrage: time to perform calculation is 0.005285501480102539
2022-09-17 16:29:37,469 - kucoin: initial amount is 30
2022-09-17 16:29:37,469 - kucoin: for PEEL-USDT price is 0.114 and quantity is 263.1578947368421
2022-09-17 16:29:37,477 - Kucoin: PEEL-USDT:fake order Buy done for a quantity of 263.0 PEEL-USDT at price 0.114
2022-09-17 16:29:37,480 - kucoin time to perform trade PEEL-USDT is 0.008015632629394531
2022-09-17 16:29:37,873 - kucoin: for PEEL-BTC price is 7.002e-06 and quantity is 263.1578947368421
2022-09-17 16:29:37,876 - Kucoin: PEEL-BTC:fake order Sell done for a quantity of 263.0 PEEL-BTC at price 7.002e-06
2022-09-17 16:29:37,876 - kucoin time to perform trade PEEL-BTC is 0.0031669139862060547
2022-09-17 16:29:38,164 - kucoin: for BTC-USDT price is 19944.0 and quantity is 1.4e-07
2022-09-17 16:29:38,167 - Kucoin: BTC-USDT:fake order Sell done for a quantity of 0.0 BTC-USDT at price 19944.0
2022-09-17 16:29:38,168 - kucoin time to perform trade BTC-USDT is 0.003412961959838867
2022-09-17 16:29:38,168 - do_arbitrage: time to perform all arbitrage is 0.7063100337982178


2022-09-17 20:17:59,402 - kucoin PROFIT-20:17:59:BUY_SELL_SELL, PEEL-USDT,PEEL-BTC,BTC-USDT, Profit/Loss: 6.832PEEL-USDT: 0.1129, PEEL-BTC: 6.912e-06, BTC-USDT: 20053.6
2022-09-17 20:17:59,403 - do_arbitrage: time to perform calculation is 0.0048558712005615234
2022-09-17 20:17:59,404 - kucoin: initial amount is 30
2022-09-17 20:17:59,404 - kucoin: for PEEL-USDT price is 0.1129 and quantity is 265.72187776793623
2022-09-17 20:17:59,412 - Kucoin: PEEL-USDT:fake order Buy done for a quantity of 265.0 PEEL-USDT at price 0.1129
2022-09-17 20:17:59,413 - kucoin time to perform trade PEEL-USDT is 0.008426904678344727
2022-09-17 20:17:59,795 - kucoin: for PEEL-BTC price is 6.912e-06 and quantity is 265.72187776793623
2022-09-17 20:17:59,798 - Kucoin: PEEL-BTC:fake order Sell done for a quantity of 265.0 PEEL-BTC at price 6.912e-06
2022-09-17 20:17:59,799 - kucoin time to perform trade PEEL-BTC is 0.003627777099609375
2022-09-17 20:18:00,085 - kucoin: for BTC-USDT price is 20053.6 and quantity is 1.4e-07
2022-09-17 20:18:00,088 - Kucoin: BTC-USDT:fake order Sell done for a quantity of 0.0 BTC-USDT at price 20053.6
2022-09-17 20:18:00,088 - kucoin time to perform trade BTC-USDT is 0.0029883384704589844
2022-09-17 20:18:00,088 - do_arbitrage: time to perform all arbitrage is 0.6921656131744385

{'id': '6326227f9ab3cd0001b420b3', 'type': 'message', 'topic': '/account/balance', 
	'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.balance', 
	'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75207399777891638', 'availableChange': '-18.942590667', 
	'currency': 'USDT', 'hold': '18.942590667', 'holdChange': '18.942590667', 
	'relationContext': {'symbol': 'BTC-USDT', 'orderId': '6326227f9ab3cd0001b420b0'}, 'relationEvent': 'trade.hold', 
	'relationEventId': '6326227f9ab3cd0001b420b3', 'time': '1663443583755', 'total': '75.69466466477891638'}}

{'id': '6326227f9ab3cd0001b420b3', 'type': 'message', 'topic': '/account/snapshotBalance', 'userId': '60ff0f7f795dce000646ae09', 
	'channelType': 'private', 'subject': 'account.snapshotBalance', 
	'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75207399777891638', 'availableChange': '-18.942590667', 
	'currency': 'USDT', 'hold': '18.942590667', 'holdChange': '18.942590667', 'relationContext': {}, 'relationEvent': 'trade.hold', 
	'relationEventId': '6326227f9ab3cd0001b420b3', 'time': '1663443583755', 'total': '75.69466466477891638'}}

{'type': 'message', 'topic': '/spotMarket/tradeOrders', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'orderChange', 'data': {'symbol': 'BTC-USDT', 'orderType': 'market', 'side': 'buy', 'orderId': '6326227f9ab3cd0001b420b0', 'liquidity': 'taker', 'type': 'match', 'orderTime': 1663443583763035336, 'filledSize': '0.00094528', 'remainFunds': '0.000012152', 'funds': '18.923667', 'matchPrice': '20019.1', 'matchSize': '0.00094528', 'tradeId': '6326227f2e113d2923d26be0', 'remainSize': '0', 'status': 'match', 'ts': 1663443583763035336}}
{'type': 'message', 'topic': '/spotMarket/tradeOrders', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'orderChange', 'data': {'symbol': 'BTC-USDT', 'orderType': 'market', 'side': 'buy', 'orderId': '6326227f9ab3cd0001b420b0', 'type': 'canceled', 'orderTime': 1663443583763035336, 'filledSize': '0.00094528', 'remainFunds': '0', 'funds': '18.923667', 'remainSize': '0', 'status': 'done', 'ts': 1663443583763035336}}

{'id': '6326227faf72a1000194ed48', 'type': 'message', 'topic': '/account/balance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.balance', 'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75207399777891638', 'availableChange': '0', 'currency': 'USDT', 'hold': '0.000012164152', 'holdChange': '-18.942578502848', 'relationContext': {'symbol': 'BTC-USDT', 'orderId': '6326227f9ab3cd0001b420b0', 'tradeId': '6326227f2e113d2923d26be0'}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227faf72a1000194ed48', 'time': '1663443583797', 'total': '56.75208616193091638'}}
{'id': '6326227faf72a1000194ed48', 'type': 'message', 'topic': '/account/snapshotBalance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.snapshotBalance', 'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75207399777891638', 'availableChange': '0', 'currency': 'USDT', 'hold': '0.000012164152', 'holdChange': '-18.942578502848', 'relationContext': {}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227faf72a1000194ed48', 'time': '1663443583797', 'total': '56.75208616193091638'}}
{'id': '6326227faf72a1000194ed47', 'type': 'message', 'topic': '/account/balance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.balance', 'data': {'accountId': '619ea6b67d983800012303fe', 'available': '0.0009477454384675568', 'availableChange': '0.00094528', 'currency': 'BTC', 'hold': '0', 'holdChange': '0', 'relationContext': {'symbol': 'BTC-USDT', 'orderId': '6326227f9ab3cd0001b420b0', 'tradeId': '6326227f2e113d2923d26be0'}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227faf72a1000194ed47', 'time': '1663443583798', 'total': '0.0009477454384675568'}}
{'id': '6326227faf72a1000194ed47', 'type': 'message', 'topic': '/account/snapshotBalance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.snapshotBalance', 'data': {'accountId': '619ea6b67d983800012303fe', 'available': '0.0009477454384675568', 'availableChange': '0.00094528', 'currency': 'BTC', 'hold': '0', 'holdChange': '0', 'relationContext': {}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227faf72a1000194ed47', 'time': '1663443583798', 'total': '0.0009477454384675568'}}

{'type': 'message', 'topic': '/spot/tradeFills', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': '/spot/tradeFills', 'data': {'fee': 0.018923654848, 'feeCurrency': 'USDT', 'feeRate': 0.001, 'orderId': '6326227f9ab3cd0001b420b0', 'orderType': 'market', 'price': 20019.1, 'side': 'buy', 'size': 0.00094528, 'symbol': 'BTC-USDT', 'time': 1663443583763035336, 'tradeId': '6326227f2e113d2923d26be0'}}

{'id': '6326227f9ab3cd0001b420b4', 'type': 'message', 'topic': '/account/balance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.balance', 'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75208616193091638', 'availableChange': '0.000012164152', 'currency': 'USDT', 'hold': '0', 'holdChange': '-0.000012164152', 'relationContext': {'symbol': 'BTC-USDT', 'orderId': '6326227f9ab3cd0001b420b0'}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227f9ab3cd0001b420b4', 'time': '1663443583816', 'total': '56.75208616193091638'}}
{'id': '6326227f9ab3cd0001b420b4', 'type': 'message', 'topic': '/account/snapshotBalance', 'userId': '60ff0f7f795dce000646ae09', 'channelType': 'private', 'subject': 'account.snapshotBalance', 'data': {'accountId': '60ff21e369821300067a866c', 'available': '56.75208616193091638', 'availableChange': '0.000012164152', 'currency': 'USDT', 'hold': '0', 'holdChange': '-0.000012164152', 'relationContext': {}, 'relationEvent': 'trade.setted', 'relationEventId': '6326227f9ab3cd0001b420b4', 'time': '1663443583816', 'total': '56.75208616193091638'}}

{'type': 'message', 'topic': '/market/ticker:BTC-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '20561.2', 'bestAskSize': '0.00036908', 'bestBid': '20560.4', 'bestBidSize': '0.00018332', 'price': '20560.4', 'sequence': '805404220', 'size': '0.00001224', 'time': 1666886381346}}
{'type': 'message', 'topic': '/market/ticker:NKN-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.088173', 'bestAskSize': '1601', 'bestBid': '0.087849', 'bestBidSize': '1506.3772', 'price': '0.087848', 'sequence': '9181618', 'size': '5.2664', 'time': 1666886373780}}
{'type': 'message', 'topic': '/market/ticker:MTV-ETH', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0000007472', 'bestAskSize': '4153.3424', 'bestBid': '0.0000007038', 'bestBidSize': '7372', 'price': '0.0000007233', 'sequence': '66681704', 'size': '373.2891', 'time': 1666886108038}}
{'type': 'message', 'topic': '/market/ticker:FORESTPLUS-BTC', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0000002537', 'bestAskSize': '771.1356', 'bestBid': '0.0000002527', 'bestBidSize': '1443.7376', 'price': '0.0000002537', 'sequence': '25847478', 'size': '4.6539', 'time': 1666886344391}}
{'type': 'message', 'topic': '/market/ticker:TOWER-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.004962', 'bestAskSize': '2069.8537', 'bestBid': '0.004961', 'bestBidSize': '2593.2893', 'price': '0.004961', 'sequence': '28742396', 'size': '1870.5951', 'time': 1666886379673}}
{'type': 'message', 'topic': '/market/ticker:FORESTPLUS-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0052102', 'bestAskSize': '11055.9498', 'bestBid': '0.0052076', 'bestBidSize': '4401.6431', 'price': '0.0052095', 'sequence': '26894963', 'size': '21355.2164', 'time': 1666886375383}}
{'type': 'message', 'topic': '/market/ticker:USDC-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.99978', 'bestAskSize': '476756.6947', 'bestBid': '0.99977', 'bestBidSize': '658053.7298', 'price': '0.99978', 'sequence': '12101243', 'size': '2.0931', 'time': 1666886367738}}
{'type': 'message', 'topic': '/market/ticker:BTC-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '20561.2', 'bestAskSize': '0.00036908', 'bestBid': '20560.4', 'bestBidSize': '0.00018332', 'price': '20560.4', 'sequence': '805404264', 'size': '0.00001224', 'time': 1666886381346}}
{'type': 'message', 'topic': '/market/ticker:ETH-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '1543.98', 'bestAskSize': '0.0149608', 'bestBid': '1543.86', 'bestBidSize': '0.0001925', 'price': '1543.74', 'sequence': '791011650', 'size': '0.0001', 'time': 1666886381448}}
{'type': 'message', 'topic': '/market/ticker:MTV-ETH', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0000007472', 'bestAskSize': '4153.3424', 'bestBid': '0.0000007038', 'bestBidSize': '7372', 'price': '0.0000007233', 'sequence': '66681708', 'size': '373.2891', 'time': 1666886108038}}
{'type': 'message', 'topic': '/market/ticker:NKN-BTC', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.00000442', 'bestAskSize': '466.7329', 'bestBid': '0.00000427', 'bestBidSize': '1467.2382', 'price': '0.00000432', 'sequence': '11260902', 'size': '159.2284', 'time': 1666876406353}}
{'type': 'message', 'topic': '/market/ticker:NKN-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.088173', 'bestAskSize': '1601', 'bestBid': '0.087849', 'bestBidSize': '1506.3772', 'price': '0.087848', 'sequence': '9181619', 'size': '5.2664', 'time': 1666886373780}}
{'type': 'message', 'topic': '/market/ticker:STORE-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.03781', 'bestAskSize': '55.1726', 'bestBid': '0.0375', 'bestBidSize': '0.5535', 'price': '0.03754', 'sequence': '27077940', 'size': '543.9386', 'time': 1666886381436}}
{'type': 'message', 'topic': '/market/ticker:DAPPT-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0008571', 'bestAskSize': '24470.6747', 'bestBid': '0.000855', 'bestBidSize': '0.0005', 'price': '0.0008566', 'sequence': '14601247', 'size': '148.4294', 'time': 1666886211647}}
{'type': 'message', 'topic': '/market/ticker:STORE-ETH', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.00002444', 'bestAskSize': '1631.4214', 'bestBid': '0.00002419', 'bestBidSize': '37.9462', 'price': '0.00002425', 'sequence': '28525293', 'size': '502.1502', 'time': 1666886378935}}
{'type': 'message', 'topic': '/market/ticker:BTC-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '20561.9', 'bestAskSize': '0.0029686', 'bestBid': '20561.2', 'bestBidSize': '0.00019481', 'price': '20561.2', 'sequence': '805404339', 'size': '0.00036', 'time': 1666886381560}}
{'type': 'message', 'topic': '/market/ticker:FORESTPLUS-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.0052102', 'bestAskSize': '11055.9498', 'bestBid': '0.0052076', 'bestBidSize': '4401.6431', 'price': '0.0052095', 'sequence': '26894965', 'size': '21355.2164', 'time': 1666886375383}}
{'type': 'message', 'topic': '/market/ticker:USDC-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '0.99978', 'bestAskSize': '476756.6947', 'bestBid': '0.99977', 'bestBidSize': '658053.7298', 'price': '0.99978', 'sequence': '12101244', 'size': '2.0931', 'time': 1666886367738}}
{'type': 'message', 'topic': '/market/ticker:ETH-USDT', 'subject': 'trade.ticker', 'data': {'bestAsk': '1543.98', 'bestAskSize': '0.0149608', 'bestBid': '1543.86', 'bestBidSize': '0.0000025', 'price': '1543.74', 'sequence': '791011681', 'size': '0.0001', 'time': 1666886381448}}



2022-10-25 23:02:19,465 - kucoin PROFIT-23:02:19:BUY_SELL_SELL, YFDAI-USDT,YFDAI-BTC,BTC-USDT, Profit/Loss: 2.242YFDAI-USDT: 41.59, YFDAI-BTC: 0.002216, BTC-USDT: 20170.6
2022-10-25 23:02:19,465 - do_arbitrage: time to perform calculation is 0.0003070831298828125
2022-10-25 23:02:19,466 - kucoin: initial amount is 30
2022-10-25 23:02:19,466 - kucoin: for YFDAI-USDT price is 41.59 and quantity is 0.7213272421255109
2022-10-25 23:02:19,839 - Kucoin: YFDAI-USDT: real buy order done for quantity: 0.7213, struct is {'orderId': '63584edb25a4860001e2e74f'}
2022-10-25 23:02:19,840 - kucoin time to perform trade YFDAI-USDT is 0.37383198738098145
2022-10-25 23:02:19,841 - kucoin: for YFDAI-BTC price is 0.002216 and quantity is 0.7213272421255109
2022-10-25 23:02:20,095 - Kucoin: YFDAI-BTC: real sell order donefor quantity: 0.7213, struct is {'orderId': '63584edbddfbb30001827903'}
2022-10-25 23:02:20,095 - kucoin time to perform trade YFDAI-BTC is 0.25400781631469727
2022-10-25 23:02:20,097 - kucoin: for BTC-USDT price is 20170.6 and quantity is 0.0015984611685501322
2022-10-25 23:02:20,329 - Kucoin - error on trade for quantity: 0.00159 and 5, algo stopped, KucoinAPIException KucoinAPIException 200004: Balance insufficient!
2022-10-25 23:02:20,329 - kucoin time to perform trade BTC-USDT is 0.23195600509643555
2022-10-25 23:02:20,329 - do_arbitrage: time to perform all arbitrage is 0.8649246692657471

2022-10-26 07:43:56,739 - kucoin PROFIT-07:43:56:BUY_SELL_SELL, EDG-USDT,EDG-BTC,BTC-USDT, Profit/Loss: 2.505EDG-USDT: 0.000907, EDG-BTC: 4.87e-08, BTC-USDT: 20179.4
2022-10-26 07:43:56,739 - do_arbitrage: time to perform calculation is 0.00032973289489746094
2022-10-26 07:43:56,739 - kucoin: initial amount is 30
2022-10-26 07:43:56,740 - kucoin: for EDG-USDT price is 0.000907 and quantity is 33076.0749724366
2022-10-26 07:43:57,106 - Kucoin: EDG-USDT: real buy order done for quantity: 33000.0, struct is {'orderId': '6358c91cddfca80001b4e55c'}
2022-10-26 07:43:57,107 - kucoin time to perform trade EDG-USDT is 0.36718201637268066
2022-10-26 07:43:57,109 - kucoin: for EDG-BTC price is 4.87e-08 and quantity is 33076.0749724366
2022-10-26 07:43:57,339 - Kucoin - error on trade for quantity: 33076.0 and 0, algo stopped, KucoinAPIException KucoinAPIException 200004: Balance insufficient!
2022-10-26 07:43:57,339 - kucoin time to perform trade EDG-BTC is 0.23073315620422363
2022-10-26 07:43:57,341 - kucoin: for BTC-USDT price is 20179.4 and quantity is 0.0016108048511576625
2022-10-26 07:43:57,341 - kucoin time to perform trade BTC-USDT is 0.0002980232238769531
2022-10-26 07:43:57,342 - do_arbitrage: time to perform all arbitrage is 0.6033306121826172
2022-10-26 07:43:57,342 - do_arbitrage: test in arbitrage function to stop run_algo after one arbitrage run, algo is False
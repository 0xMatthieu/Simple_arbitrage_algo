# Crypto_arbitrage_bot

how to start
run python My_discord.py

# what should it do ?

Goal is to provide an arbitrage bot on predefined CEX (centralized exchange). The software implements an abstraction layer to separate logic from IO (in this case requests to CEX)
There is 3 different functions executed:
- a discord bot to implement a kind of remote session. Mainly used to get notified for each events, but could be used to also interact with the bot
- an abitrage function which has 2 purposes (depending on the field "job")
  - the first one is to use REST API to fetch all crypto prices and try to find arbitrage opportunity. The REST API rate is too slow to execute all trades (2s refreshing rate). Instead the function fill a list (a JSON file) with all opportunities found
  - the second one opens a websocket to subscribe to all pairs listed in the JSON file, looks over the list and perform arbitrage trade if an opportunity exists. Web socket refresh rate is faster (<150 ms)
  
 # general information
  - CEX implements around 1200 crypto trading pairs but websocket API allows only 100 requests https://docs.kucoin.com/#request-rate-limit 
  
  ![image](https://user-images.githubusercontent.com/111059326/186150000-cbbfaf66-9fcf-4032-8096-313703da779c.png)


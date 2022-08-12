#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""


import pandas as pd
import logging
import settings_binance as sb
import settings_kucoin as sk
import Binance_trade
import Kucoin_trade
import pandas_ta as ta
import Trade_algo
from datetime import datetime
import time



def get_crypto_combinations(pairs, base, df_all_combinations):
	#pairs shall be a dataframe
	#sb.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
	df_dict = pairs.to_dict('records')
	for row in df_dict:
		add_to_list = True
		#print(f"quote asset 1 {row['quoteAsset']}")
		if (row['quoteAsset'] == base):
			for row2 in df_dict:
				#print(f"quote asset 1 {row2['quoteAsset']}")
				if (row['baseAsset'] == row2['quoteAsset']):
					for row3 in df_dict:
						#print(f"quote asset 1 {row3['quoteAsset']}")
						if((row2['baseAsset'] == row3['baseAsset']) and (row3['quoteAsset'] == row['quoteAsset'])):
							combination = pd.DataFrame({"base":[row['quoteAsset']]
								,"intermediate":[row['baseAsset']]
								,"ticker":[row2['baseAsset']]
								,"first_pair":[row['symbol']]
								,"second_pair":[row2['symbol']]
								,"third_pair":[row3['symbol']]
							})
							#print(f"combination {combination}")
							#add only combination with fiat allowed, delete others
							#for fiat in sb.fiat_list:
							#	if combination['base'][0] == fiat or combination['intermediate'][0] == fiat or combination['ticker'][0] == fiat: 
							#		add_to_list = False
							#for crypto in sb.crypto_list:
							#	if combination['base'][0] == crypto or combination['intermediate'][0] == crypto or combination['ticker'][0] == crypto: 
							#		add_to_list = False
							if row['status'] != 'TRADING' or row2['status'] != 'TRADING' or row3['status'] != 'TRADING':
								add_to_list = False

							if add_to_list == True:
								df_all_combinations = df_all_combinations.append(combination)
								#print(f"combination is {combination} and total is {df_all_combinations}")

	df_unique_currencies = pd.DataFrame((df_all_combinations['first_pair'].append(df_all_combinations['second_pair']).append(df_all_combinations['third_pair'])).unique())
	dict_all_combinations = df_all_combinations.to_dict('records')

	return df_all_combinations, df_unique_currencies, dict_all_combinations


def check_buy_buy_sell(scrip1, scrip2, scrip3, price_list, initial_investment, exchange): 
	## SCRIP1
	investment_amount1 = initial_investment
	current_price1 = Trade_algo.fetch_price_exchange(exchange, scrip1, price_list, 'buy')
	final_price = 0
	scrip_prices = {}
    
	if current_price1 is not None:
		buy_quantity1 = round(investment_amount1 / current_price1, 8)
		#time.sleep(1)
        ## SCRIP2
		investment_amount2 = buy_quantity1     
		current_price2 = Trade_algo.fetch_price_exchange(exchange, scrip2, price_list, 'buy')
		if current_price2 is not None:
			buy_quantity2 = round(investment_amount2 / current_price2, 8)
			#time.sleep(1)
            ## SCRIP3
			investment_amount3 = buy_quantity2     
			current_price3 = Trade_algo.fetch_price_exchange(exchange, scrip3, price_list, 'sell')
			if current_price3 is not None:
				sell_quantity3 = buy_quantity2
				final_price = round(sell_quantity3 * current_price3,3)
				scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}
                
	return final_price, scrip_prices

def check_buy_sell_sell(scrip1, scrip2, scrip3, price_list, initial_investment, exchange):
	## SCRIP1
	investment_amount1 = initial_investment
	current_price1 = Trade_algo.fetch_price_exchange(exchange, scrip1, price_list, 'buy')
	final_price = 0
	scrip_prices = {}
	if current_price1 is not None:
		buy_quantity1 = round(investment_amount1 / current_price1, 8)
		#time.sleep(1)
        ## SCRIP2
		investment_amount2 = buy_quantity1     
		current_price2 = Trade_algo.fetch_price_exchange(exchange, scrip2, price_list, 'sell')
		if current_price2 is not None:
			sell_quantity2 = buy_quantity1
			sell_price2 = round(sell_quantity2 * current_price2,8)
			#time.sleep(1)
            ## SCRIP1
			investment_amount3 = sell_price2     
			current_price3 = Trade_algo.fetch_price_exchange(exchange, scrip3, price_list, 'sell')
			if current_price3 is not None:
				sell_quantity3 = sell_price2
				final_price = round(sell_quantity3 * current_price3,3)
				scrip_prices = {scrip1 : current_price1, scrip2 : current_price2, scrip3 : current_price3}
	return final_price,scrip_prices

def check_profit_loss(total_price_after_sell,initial_investment,transaction_brokerage, min_profit):
	apprx_brokerage = transaction_brokerage * initial_investment/100 * 3
	min_profitable_price = initial_investment + apprx_brokerage + min_profit
	profit_loss = round(total_price_after_sell - min_profitable_price,3)
	return profit_loss

def place_buy_order(scrip, quantity, current_price, exchange, to_round):
	start = time.time()
	text = f"{exchange}: for {scrip} price is {current_price} and quantity is {quantity}"
	Trade_algo.send_text(text, exchange = exchange)
	if exchange == 'binance' and sb.run_algo == True:
		Binance_trade.do_market_order(scrip, order_type = "Buy", quantity = quantity, current_price = current_price, to_round = to_round)
	elif exchange == 'kucoin' and sk.run_algo == True:
		Kucoin_trade.do_market_order(scrip, order_type = "Buy", quantity = quantity, current_price = current_price, to_round = to_round)
	time_elapsed = time.time() - start
	text = f"{exchange} time to perform trade {scrip} is {time_elapsed}"
	Trade_algo.send_text(text, exchange = exchange)

def place_sell_order(scrip, quantity, current_price, exchange, to_round):
	start = time.time()
	text = f"{exchange}: for {scrip} price is {current_price} and quantity is {quantity}"
	Trade_algo.send_text(text, exchange = exchange)
	if exchange == 'binance' and sb.run_algo == True:
		Binance_trade.do_market_order(scrip, order_type = "Sell", quantity = quantity, current_price = current_price, to_round = to_round)
	elif exchange == 'kucoin' and sk.run_algo == True:
		Kucoin_trade.do_market_order(scrip, order_type = "Sell", quantity = quantity, current_price = current_price, to_round = to_round)
	time_elapsed = time.time() - start
	text = f"{exchange} time to perform trade {scrip} is {time_elapsed}"
	Trade_algo.send_text(text, exchange = exchange)

def place_trade_orders(type, scrip1, scrip2, scrip3, initial_amount, scrip_prices, exchange):
	final_amount = 0.0
	start = time.time()
	text = f"{exchange}: initial amount is {initial_amount}"
	Trade_algo.send_text(text, exchange = exchange)
	if type == 'BUY_BUY_SELL':
		s1_quantity = initial_amount/scrip_prices[scrip1]
		place_buy_order(scrip1, s1_quantity, scrip_prices[scrip1], exchange, True)
		#time.sleep(0.1)
		s1_quantity = Trade_algo.fetch_amount_exchange_order(scrip = scrip2, exchange = exchange, order = "buy")
		s2_quantity = s1_quantity/scrip_prices[scrip2]
		place_buy_order(scrip2, s2_quantity, scrip_prices[scrip2], exchange, True)
		#time.sleep(0.1)
		s2_quantity = Trade_algo.fetch_amount_exchange_order(scrip = scrip3, exchange = exchange, order = "sell")
		s3_quantity = s2_quantity
		place_sell_order(scrip3, s3_quantity, scrip_prices[scrip3], exchange, True)
        
	elif type == 'BUY_SELL_SELL':
		s1_quantity = initial_amount/scrip_prices[scrip1]
		place_buy_order(scrip1, s1_quantity, scrip_prices[scrip1], exchange, True)
		#time.sleep(0.1)
		s1_quantity = Trade_algo.fetch_amount_exchange_order(scrip = scrip2, exchange = exchange, order = "sell")
		s2_quantity = s1_quantity
		place_sell_order(scrip2, s2_quantity, scrip_prices[scrip2], exchange, True)
		#time.sleep(0.1)
		s3_quantity = Trade_algo.fetch_amount_exchange_order(scrip = scrip3, exchange = exchange, order = "sell")
		#s3_quantity = s2_quantity * scrip_prices[scrip2]
		place_sell_order(scrip3, s3_quantity, scrip_prices[scrip3], exchange, True)

def perform_triangular_arbitrage(scrip1, scrip2, scrip3, arbitrage_type,initial_investment, 
                               transaction_brokerage, min_profit, exchange, price_list):
	final_price = 0.0
	start = time.time()
	if(arbitrage_type == 'BUY_BUY_SELL'):
		# Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - BUY, scrip3 - SELL
		final_price, scrip_prices = check_buy_buy_sell(scrip1, scrip2, scrip3, price_list, initial_investment, exchange)
        
	elif(arbitrage_type == 'BUY_SELL_SELL'):
		# Check this combination for triangular arbitrage: scrip1 - BUY, scrip2 - SELL, scrip3 - SELL
		final_price, scrip_prices = check_buy_sell_sell(scrip1, scrip2, scrip3, price_list, initial_investment, exchange)
        
	profit_loss = check_profit_loss(final_price,initial_investment, transaction_brokerage, min_profit)
	#print(f"prices for {scrip1}:{scrip2}:{scrip3} are {final_price} and {scrip_prices}")
	#print(f"profit for {scrip1}:{scrip2}:{scrip3} is {profit_loss} ")

	if profit_loss>0:
		time_elapsed = time.time() - start
		text = f"{exchange} PROFIT-{datetime.now().strftime('%H:%M:%S')}:"\
			f"{arbitrage_type}, {scrip1},{scrip2},{scrip3}, Profit/Loss: {round(final_price-initial_investment,3)}"
		Trade_algo.send_text(text, exchange = exchange)
		text = f"time to perform calculation is {time_elapsed}"
		Trade_algo.send_text(text, exchange = exchange)
		place_trade_orders(arbitrage_type, scrip1, scrip2, scrip3, initial_investment, scrip_prices, exchange) 
		sb.Index += 1    
		sk.Index += 1 
		time_elapsed = time.time() - start
		text = f"time to perform all arbitrage is {time_elapsed}"
		Trade_algo.send_text(text, exchange = exchange)

if __name__ == "__main__":
   main()

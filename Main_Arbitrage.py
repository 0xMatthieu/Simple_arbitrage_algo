#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""

import settings_binance as sb
import settings_kucoin as sk
import Binance_trade
import Kucoin_trade
import Trade_algo
import Arbitrage
import time
import logging
import pandas as pd
#import My_discord
from datetime import datetime


def main(exchange = 'kucoin'):
	
	#INVESTMENT_AMOUNT_DOLLARS = 100
	MIN_PROFIT_DOLLARS = 5
	BROKERAGE_PER_TRANSACTION_PERCENT = 0.1

	Cycle_step = 0 #run as fast as possible
	Algo_step = 60*60

	Time_cycle = time.time() + Cycle_step
	Time_algo = time.time() + Algo_step

	logging.basicConfig(filename='my_log_file.log', format='%(asctime)s - %(message)s', level=logging.INFO)

	"""
	All exchanges
	"""
	sb.init()
	sk.init()

	"""
	Binance exchange
	"""
	if exchange == 'binance':
		#sb.init()
		sb.do_real_order = True
		text = f"{exchange} real order is {sb.do_real_order}"
		Trade_algo.send_text(text, exchange = exchange)
		Binance_trade.get_all_pairs()
		sb.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
		sb.df_all_combinations, sb.df_unique_currencies, sb.dict_all_combinations = Arbitrage.get_crypto_combinations(sb.df_all_pairs, "USDT", sb.df_all_combinations)
		sb.df_all_combinations, sb.df_unique_currencies, sb.dict_all_combinations = Arbitrage.get_crypto_combinations(sb.df_all_pairs, "BUSD", sb.df_all_combinations)
		sb.order_done_current_cycle = True
		#Binance_trade.money_available(Log = sb.order_done_current_cycle, Currency1 = Currency1, Currency2 = Currency2, Currency3 = Currency3, Currency4 = Currency4, Currency5= Currency5)
		#Binance_trade.futures_fiat_available(Log = sb.order_done_current_cycle)
		Binance_trade.fiat_available(Log = True)
		text = f"Start software binance -{datetime.now().strftime('%H:%M:%S')}"
		Trade_algo.send_text(text, exchange = exchange)

	"""
	Kucoin exchange
	"""
	if exchange == 'kucoin':
		#sk.init()
		sk.do_real_order = True
		text = f"{exchange} real order is {sk.do_real_order}"
		Trade_algo.send_text(text, exchange = exchange)
		Kucoin_trade.get_all_pairs()
		sk.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
		sk.df_all_combinations, sk.df_unique_currencies, sk.dict_all_combinations = Arbitrage.get_crypto_combinations(sk.df_all_pairs, "USDT", sk.df_all_combinations)
		Kucoin_trade.prepare_price_list_for_websocket()
		Kucoin_trade.start_websocket()
		text = f"Start software kucoin -{datetime.now().strftime('%H:%M:%S')}"
		Trade_algo.send_text(text, exchange = exchange)


	logging.info(f" start program at : {pd.Timestamp.now()}")
	logging.critical(f" ---------------------------------------------------------------------")
	logging.critical(f" ----------------------------- start software ------------------------")
	logging.critical(f" ---------------------------------------------------------------------")
	logging.critical(f" Start software -{datetime.now().strftime('%H:%M:%S')}")

	

	Run_loop = True
	Crypto_loop = 100000000

	#Currency1 = sb.Currency('BTCUSDT', 'BTC')
	#Binance_trade.start_to_get_data(Currency1)

	#My_discord.init()

	while Run_loop:

		start = time.time()

		if exchange == 'binance':
			sb.Index = 0


		if time.time() > Time_algo:
			Time_algo = time.time() + Algo_step
			"""
			Binance exchange
			"""
			if exchange == 'binance':
				Binance_trade.get_all_pairs()
				sb.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
				sb.df_all_combinations, sb.df_unique_currencies, sb.dict_all_combinations = Arbitrage.get_crypto_combinations(sb.df_all_pairs, "USDT", sb.df_all_combinations)
				sb.df_all_combinations, sb.df_unique_currencies, sb.dict_all_combinations = Arbitrage.get_crypto_combinations(sb.df_all_pairs, "BUSD", sb.df_all_combinations)

			"""
			Kucoin exchange
			"""
			if exchange == 'kucoin':
				Kucoin_trade.get_all_pairs()
				sk.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
				sk.df_all_combinations, sk.df_unique_currencies, sk.dict_all_combinations = Arbitrage.get_crypto_combinations(sk.df_all_pairs, "USDT", sk.df_all_combinations)
				Kucoin_trade.prepare_price_list_for_websocket()

		if time.time() > Time_cycle:
			Time_cycle = time.time() + Cycle_step

			"""
			Binance exchange
			"""
			if exchange == 'binance' and sb.run_algo == True:
				sb.order_done_current_cycle = False
				INVESTMENT_AMOUNT_DOLLARS = sb.current_money_available
				"""
				to do: optimize this part, else all invest are based on this value whatever real amount is
				"""
				INVESTMENT_AMOUNT_DOLLARS = 30
				MIN_PROFIT_DOLLARS = 2
				Binance_trade.get_all_prices()

				
				for row in sb.dict_all_combinations:
				#for combination in wx_combinations_usdt:

					base = row['base']
					intermediate = row['intermediate']
					ticker = row['ticker']


					s1 = row['first_pair']			# Eg: BTC/USDT
					s2 = row['second_pair']			# Eg: ETH/BTC
					s3 = row['third_pair']			# Eg: ETH/USDT 

					# Check triangular arbitrage for buy-buy-sell 
					Arbitrage.perform_triangular_arbitrage(s1,s2,s3,'BUY_BUY_SELL',INVESTMENT_AMOUNT_DOLLARS,
											BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, sb.all_prices)
				    # Check triangular arbitrage for buy-sell-sell 
					Arbitrage.perform_triangular_arbitrage(s3,s2,s1,'BUY_SELL_SELL',INVESTMENT_AMOUNT_DOLLARS,
											BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, sb.all_prices)
					Binance_trade.fiat_available(Log = sb.order_done_current_cycle)


					if sb.Index == Crypto_loop:
						break

			"""
			Kucoin exchange
			"""
			if exchange == 'kucoin' and sk.run_algo == True:
				sk.order_done_current_cycle = False
				INVESTMENT_AMOUNT_DOLLARS = sk.current_money_available
				INVESTMENT_AMOUNT_DOLLARS = 22
				MIN_PROFIT_DOLLARS = 2
				#Kucoin_trade.get_all_prices()

				
				for row in sk.dict_all_combinations:
				#for combination in wx_combinations_usdt:

					base = row['base']
					intermediate = row['intermediate']
					ticker = row['ticker']


					s1 = row['first_pair']			# Eg: BTC/USDT
					s2 = row['second_pair']			# Eg: ETH/BTC
					s3 = row['third_pair']			# Eg: ETH/USDT 

					#print(f"{s1} / {s2} / {s3}")

					# Check triangular arbitrage for buy-buy-sell 
					Arbitrage.perform_triangular_arbitrage(s1,s2,s3,'BUY_BUY_SELL',INVESTMENT_AMOUNT_DOLLARS,
											BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, sk.all_prices_websocket)
				    # Check triangular arbitrage for buy-sell-sell 
					Arbitrage.perform_triangular_arbitrage(s3,s2,s1,'BUY_SELL_SELL',INVESTMENT_AMOUNT_DOLLARS,
											BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, sk.all_prices_websocket)
					Kucoin_trade.fiat_available(Log = sb.order_done_current_cycle)


					if sk.Index == Crypto_loop:
						break

			end = time.time()
			time_elapsed = end - start
			#print(f"{exchange} time elapsed is {time_elapsed}")
			#Last_info_to_send = str(time_elapsed)
			Run_loop = True


if __name__ == "__main__":
	main()

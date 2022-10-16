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
import numpy as np

from datetime import datetime
import asyncio
import concurrent.futures




def init(exchange = 'kucoin', job = 'get_list'):
	
	Cycle_step = 0 #run as fast as possible
	Algo_step = 60*60

	Time_cycle = time.time() + Cycle_step
	Time_algo = time.time() + Algo_step

	logging.basicConfig(filename='my_log_file.log', format='%(asctime)s - %(message)s', level=logging.INFO)

	"""
	All exchanges
	"""
	#sb.init()
	#sk.init()

	"""
	Binance exchange
	"""
	if exchange == 'binance':
		#sb.init()
		#sb.do_real_order = True
		text = f"{exchange} real order is {sb.do_real_order} and job is {job}"
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
		sk.arbitrage_opportunity = pd.read_json('Arbitrage_oppotunities.json')
		#sk.init()
		#sk.do_real_order = False
		text = f"{exchange} real order is {sk.do_real_order} and job is {job}"
		Trade_algo.send_text(text, exchange = exchange)
		Kucoin_trade.get_all_pairs()
		sk.df_all_combinations = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
		sk.df_all_combinations, sk.df_unique_currencies, sk.dict_all_combinations = Arbitrage.get_crypto_combinations(sk.df_all_pairs, "USDT", sk.df_all_combinations)
		
		Kucoin_trade.prepare_price_list_for_websocket()
		sk.df_all_combinations_arbitrage = pd.DataFrame(columns=['base', 'intermediate', 'ticker', 'first_pair', 'second_pair', 'third_pair'])
		sk.df_all_combinations_arbitrage, sk.df_unique_currencies_arbitrage, sk.dict_all_combinations_arbitrage = Arbitrage.get_crypto_combinations(sk.df_all_pairs_arbitrage, "USDT", sk.df_all_combinations_arbitrage)
		
		#Kucoin_trade.start_websocket()
		text = f"Start software kucoin -{datetime.now().strftime('%H:%M:%S')}"
		Trade_algo.send_text(text, exchange = exchange)


	logging.info(f" start program at : {pd.Timestamp.now()}")
	logging.critical(f" ---------------------------------------------------------------------")
	logging.critical(f" ----------------------------- start software ------------------------")
	logging.critical(f" ---------------------------------------------------------------------")
	logging.critical(f" Start software -{datetime.now().strftime('%H:%M:%S')}")


def update_list(exchange = 'kucoin'):

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

def perform_arbitrage(dict_crypto = None, exchange = 'kucoin', job = 'get_list', price_list = None):

	sk.order_done_current_cycle = False
	INVESTMENT_AMOUNT_DOLLARS = sk.current_money_available
	INVESTMENT_AMOUNT_DOLLARS = 30
	MIN_PROFIT_DOLLARS = 2
	BROKERAGE_PER_TRANSACTION_PERCENT = 0.1



	if dict_crypto is not None:
		#for row in zip(*dict_crypto.values()):
		#for row in dict_crypto:
		#print(f"start perform_arbitrage process and {len(dict_crypto)} ")

		for row in zip(dict_crypto):

			base = row[0]['base']
			intermediate = row[0]['intermediate']
			ticker = row[0]['ticker']


			s1 = row[0]['first_pair']			# Eg: BTC/USDT
			s2 = row[0]['second_pair']			# Eg: ETH/BTC
			s3 = row[0]['third_pair']			# Eg: ETH/USDT 

			#print(f"{s1} / {s2} / {s3}")

			# Check triangular arbitrage for buy-buy-sell 
			Arbitrage.perform_triangular_arbitrage(s1,s2,s3,'BUY_BUY_SELL',INVESTMENT_AMOUNT_DOLLARS,
									BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, price_list, job)
			# Check triangular arbitrage for buy-sell-sell 
			Arbitrage.perform_triangular_arbitrage(s3,s2,s1,'BUY_SELL_SELL',INVESTMENT_AMOUNT_DOLLARS,
									BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, price_list, job)

			"""
			if exchange == 'binance':
				Binance_trade.fiat_available(Log = sb.order_done_current_cycle)
			elif exchange == 'kucoin':
				Kucoin_trade.fiat_available(Log = sb.order_done_current_cycle)
			"""

def run(exchange = 'kucoin', job = 'get_list', num_procs = 2):

	#print(f"{exchange}: {job} index arbitrage is {sk.index_arbitrage} and shared index is {sk.index.value}")
	if sk.index_arbitrage >= int(sk.index.value):
		return
	else:
		sk.index_arbitrage = int(sk.index.value)


	start = time.time()

	Trade_algo.update_process_data('kucoin', 'arbitrage')

	#print(f"{exchange}: {job} dict is {sk.all_prices_websocket['price'].to_numpy()[sk.all_prices_websocket['symbol'].to_numpy() == 'BTC-USDT']}")
	#print(f"{exchange}: {job} client is {sk.client}")

	"""
	Binance exchange
	"""
	if exchange == 'binance':
		run_algo = sb.run_algo
		sb.order_done_current_cycle = False
		exchange_dict = sb.dict_all_combinations

		if job == 'get_list':
			Binance_trade.get_all_prices()
			price_list = sb.all_prices
		elif job == 'do_arbitrage':
			Binance_trade.get_all_prices()
			price_list = sb.all_prices

	"""
	Kucoin exchange
	"""
	if exchange == 'kucoin':
		run_algo = sk.run_algo
		sk.order_done_current_cycle = False
		

		if job == 'get_list':
			exchange_dict = sk.dict_all_combinations
			Kucoin_trade.get_all_prices()
			price_list = sk.all_prices
		elif job == 'do_arbitrage':
			Kucoin_trade.check_if_websocket_is_running()
			exchange_dict = sk.dict_all_combinations_arbitrage
			price_list = sk.all_prices_websocket
			#print(f"verification passed")

	# main software: use concurrent futures
	if run_algo:

		perform_arbitrage(dict_crypto=exchange_dict, exchange=exchange, job=job, price_list=price_list)
		"""
		splitted_df = np.array_split(exchange_dict, num_procs)

		df_results = []

		with concurrent.futures.ProcessPoolExecutor(max_workers=num_procs) as executor:
			results = [executor.submit(perform_arbitrage,dict_crypto=df, exchange=exchange, job=job, price_list=price_list) for df in splitted_df]

			for result in concurrent.futures.as_completed(results):
				try:
					df_results.append(result.result())
				except Exception as ex:
					print(str(ex))
					pass
		"""
		
	end = time.time()
	time_elapsed = end - start
	#print(f"{exchange}: {job} time elapsed is {time_elapsed} and run algo is {run_algo} and index is {sk.index_arbitrage}")



if __name__ == "__main__":
	main()

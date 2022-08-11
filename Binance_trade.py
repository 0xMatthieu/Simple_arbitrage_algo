#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""


import time

from binance.exceptions import BinanceAPIException, BinanceOrderException, BinanceWebsocketUnableToConnect
from binance import ThreadedWebsocketManager, Client, ThreadedDepthCacheManager
import pandas as pd
import logging
import settings_binance as sb 
import math
import requests
import Trade_algo
from datetime import datetime


def start_to_get_data(Currency):
	# start is required to initialise its internal loop
	Currency.twm = ThreadedWebsocketManager(api_key=sb.api_key, api_secret=sb.api_secret)
	Currency.twm.start()
	
	def btc_pairs_trade(msg):
		''' define how to process incoming WebSocket messages '''
		if msg['e'] != 'error':

			#print(f"{pd.Timestamp.now()}: websocket price of {Currency.Currency_crypto} is: {float(msg['k']['c'])} while current price is {Currency.current_price}")
			Currency.price[Currency.Currency].loc[len(Currency.price[Currency.Currency])] = [pd.Timestamp.now(), float(msg['k']['c'])]

			#check if price is the same
			if Currency.price['price_stuck'] > 20:
				Currency.price['error'] = True
				Currency.price['price_stuck'] = 0
			elif Currency.price['old_price'] == float(msg['k']['c']):
				Currency.price['price_stuck'] = Currency.price['price_stuck'] + 1
			else:
				Currency.price['price_stuck'] = 0
		else:
			Currency.price['error'] = True

		Currency.price['old_price'] = float(msg['k']['c'])
		
	# init and start the WebSocket
	Currency.twm.start_kline_socket(callback=btc_pairs_trade, symbol=Currency.Currency)

	## main
	while len(Currency.price[Currency.Currency]) == 0:
		# wait for WebSocket to start streaming data
		time.sleep(0.1)


def get_current_data(Currency):
	# error check to make sure WebSocket is working
	if Currency.price['error']:
		# stop and restart socket
		Currency.twm.stop()
		#time.sleep(1)

		logging.critical(f" -------------------------------error--------------------------------------")
		logging.critical(f" {Currency.Currency} price error futures")
		Currency.price['error'] = False

		start_to_get_data(Currency)


def start_to_get_order_book_depth(Currency):
	# start is required to initialise its internal loop
	Currency.dcm = ThreadedDepthCacheManager(api_key=sb.api_key, api_secret=sb.api_secret)
	Currency.dcm.start()
	
	def handle_dcm_message(depth_cache):
		Currency.top_bids = depth_cache.get_bids()[:Currency.arg_max_element]
		Currency.top_asks = depth_cache.get_asks()[:Currency.arg_max_element]
		Currency.update_time = depth_cache.update_time
		Currency.depth_message = depth_cache

		
	# init and start the WebSocket
	Currency.dcm.start_depth_cache(callback=handle_dcm_message, symbol=Currency.Currency)

#TODO -----------
def get_current_order_book(Currency):
	# error check to make sure WebSocket is working
	if Currency.price['error']:
		# stop and restart socket
		Currency.twm.stop()
		time.sleep(1)

		logging.critical(f" -------------------------------error--------------------------------------")
		logging.critical(f" {Currency.Currency} price error futures")
		Currency.price['error'] = False

		start_to_get_data(Currency)

def do_market_order(currency_name =0, order_type = "None", quantity = 0, current_price = 0, to_round = True):
	sb.order_done_current_cycle = True
	row = sb.df_all_pairs.loc[sb.df_all_pairs['symbol'] == currency_name]
	min_notional = float(row['filters'].iloc[0][3]['minNotional'])
	StepSize = float(row['filters'].iloc[0][2]['stepSize'])
	precision = int(round(-math.log(StepSize, 10), 0))
	precision = precision - 2 #found on internet, doesn't make sense ...
	if precision < 0:
		precision = 0
	fee = 0.1 * quantity * current_price
	fee = 0
	#quantity = max(round((quantity * current_price - fee) / current_price, precision), 0)
	#quantity = max(round(quantity, precision), 0)
	if to_round == True:
		quantity = max(math.floor(quantity * (1/StepSize)) / (1/StepSize), 0)
		quantity = max(round(quantity, precision), 0)
	if sb.do_real_order:
		try:
			if order_type == "Buy":
				#time.sleep(0.01)
				order = sb.client.order_market_buy(symbol=currency_name, quantity=quantity)
				text = f"{currency_name}: real buy order done for quantity: {quantity}, struct is {order}"
				Trade_algo.send_text(text, exchange = 'binance')
			elif order_type == "Sell":
				#time.sleep(0.01)
				order = sb.client.order_market_sell(symbol=currency_name, quantity=quantity)
				text = f"{currency_name}: real sell order done for quantity: {quantity}, struct is {order}"
				Trade_algo.send_text(text, exchange = 'binance')
			else:
				return
		except BinanceAPIException as e:
			# error handling goes here
			sb.run_algo = False
			text = f"Binance - error on trade, algo stopped for quantity: {quantity}, BinanceAPIException {e}"
			Trade_algo.send_text(text, exchange = 'binance')
		except BinanceOrderException as e:
			# error handling goes here
			sb.run_algo = False
			text = f"Binance - error on trade for quantity: {quantity}, algo stopped, BinanceOrderException {e}"
			Trade_algo.send_text(text, exchange = 'binance')
		except Exception as e:
			sb.run_algo = False
			text = f"Binance - error on trade for quantity: {quantity}, algo stopped, general exception {e}"
			Trade_algo.send_text(text, exchange = 'binance')

	else:
		text = f"{currency_name}:fake order {order_type} done for a quantity of {quantity} {currency_name} at price {current_price}"
		Trade_algo.send_text(text, exchange = 'binance')
		"""
		if order_type == "Buy":
			sb.current_money_available = max(sb.current_money_available - Currency.current_price * quantity, 0)
			Currency.current_crypto_available = Currency.current_crypto_available + quantity
		elif order_type == "Sell":
			sb.current_money_available = sb.current_money_available + Currency.current_price * quantity
			Currency.current_crypto_available = max(Currency.current_crypto_available - quantity, 0)
		"""

def get_currency_min_notional(Currency):
	info = sb.client.get_symbol_info(Currency.Currency)
	Currency.min_notional = float(info['filters'][3]['minNotional'])
	StepSize = float(info['filters'][2]['stepSize'])
	Currency.precision = int(round(-math.log(StepSize, 10), 0))
	Currency.precision = Currency.precision - 2 #found on internet, doesn't make sense ...
	if Currency.precision < 0:
		Currency.precision = 0
	Currency.qty_reduce_only = round(float(info['filters'][5]['maxQty'])/100, 0)

def get_all_pairs():
	info = sb.client.get_exchange_info()
	sb.df_all_pairs = pd.DataFrame(info['symbols'])
	sb.df_all_pairs = sb.df_all_pairs[['baseAsset','quoteAsset','symbol','status','filters']]

def fetch_precision(currency_name, price_list):
	row = price_list.loc[price_list['symbol'] == currency_name]
	min_notional = float(row['filters'][0][3]['minNotional'].item())
	StepSize = float(row['filters'][2]['stepSize'])
	precision = int(round(-math.log(StepSize, 10), 0))
	precision = precision - 2 #found on internet, doesn't make sense ...
	if precision < 0:
		precision = 0
	#qty_reduce_only = round(float(row['filters'][5]['maxQty'])/100, 0)
	return min_notional, precision


def create_all_currency_class():
	for index, row in sb.df_all_pairs.iterrows():
		sb.df_all_currencies.append(sb.Currency(row['symbol'], ['baseAsset']))

def get_all_prices():
	#time.sleep(0.01)
	try:
		binance_prices = pd.DataFrame(sb.client.get_all_tickers())
		sb.all_prices = binance_prices
	except requests.exceptions.Timeout:
		text = f"{datetime.now().strftime('%H:%M:%S')} binance read price timeout has occured"
		Trade_algo.send_text(text, exchange = 'binance')
	except Exception as e:
		text = f"{datetime.now().strftime('%H:%M:%S')} binance error has occured: {e}"
		Trade_algo.send_text(text, exchange = 'binance')


	sb.all_prices = pd.DataFrame(sb.client.get_all_tickers())

def get_money(Currency = "USDT"):
	amount = 'Not available'
	if sb.api_key != None:
		try:
			time.sleep(0.01)
			value = sb.client.get_asset_balance(asset=Currency)
			amount = float(value['free'])
		except BinanceAPIException as e:
			# error handling goes here
			text = f"{Currency.Currency_crypto}: BinanceAPIException during asset balance access: {e}"
			Trade_algo.send_text(text, exchange = 'binance')
		except BinanceWebsocketUnableToConnect as e:
			text = f"{Currency.Currency_crypto}: BinanceWebsocketUnableToConnect during asset balance access: {e}"
			Trade_algo.send_text(text, exchange = 'binance')
	return amount

def fiat_available(Currency = "USDT", Log = False):
	# shall be call first, reset current total
	sb.current_total = 0
	if sb.api_key != None and sb.test == False and Log == True:
		try:
			time.sleep(0.01)
			value = sb.client.get_asset_balance(asset=Currency)
			sb.current_money_available = float(value['free'])
		except BinanceAPIException as e:
			# error handling goes here
			text = f"{Currency.Currency_crypto}: BinanceAPIException during asset balance access: {e}"
			Trade_algo.send_text(text, exchange = 'binance')
		except BinanceWebsocketUnableToConnect as e:
			text = f"{Currency.Currency_crypto}: BinanceWebsocketUnableToConnect during asset balance access: {e}"
			Trade_algo.send_text(text, exchange = 'binance')
	sb.current_total = sb.current_money_available
	sb.balance = round(sb.current_total - sb.total_money_available, 2)

def fetch_current_ticker_price(currency_name, price_list):
	price_row = price_list.loc[price_list['symbol'] == currency_name]
	price = float(price_row["price"].item())
	return price


if __name__ == "__main__":
   main()

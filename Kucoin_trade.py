#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""


import time

from kucoin.client import Client
from kucoin.exceptions import KucoinAPIException, KucoinRequestException, MarketOrderException
from kucoin.asyncio import KucoinSocketManager
import asyncio
import pandas as pd
import logging
import settings_kucoin as sk
import math
import numpy as np
import requests
from datetime import datetime
import Trade_algo
from tqdm import tqdm





def do_market_order(currency_name =0, order_type = "None", quantity = 0, current_price = 0, to_round = True):
	sk.order_done_current_cycle = True
	row = sk.df_all_pairs.loc[sk.df_all_pairs['symbol'] == currency_name]
	min_notional = float(row['minNotional'])
	StepSize = float(row['stepSize'])
	precision = int(round(-math.log(StepSize, 10), 0))
	#precision = precision - 2 #found on internet, doesn't make sense ...
	if precision < 0:
		precision = 0
	fee = 0.1 * quantity * current_price
	fee = 0
	#quantity = max(round((quantity * current_price - fee) / current_price, precision), 0)
	#quantity = max(round(quantity, precision), 0)
	if to_round == True:
		quantity = max(math.floor(quantity * (1/StepSize)) / (1/StepSize), 0)
		quantity = max(round(quantity, precision), 0)
	if sk.do_real_order:
		try:
			if order_type == "Buy":
				#time.sleep(0.01)
				order = sk.client.create_market_order(symbol=currency_name, side=sk.client.SIDE_BUY, size=quantity)
				text = f"Kucoin: {currency_name}: real buy order done for quantity: {quantity}, struct is {order}"
				Trade_algo.send_text(text, exchange = 'kucoin')
			elif order_type == "Sell":
				#time.sleep(0.01)
				order = sk.client.create_market_order(symbol=currency_name, side=sk.client.SIDE_SELL, size=quantity)
				text = f"Kucoin: {currency_name}: real sell order donefor quantity: {quantity}, struct is {order}"
				Trade_algo.send_text(text, exchange = 'kucoin')
			else:
				return
		except KucoinAPIException as e:
			# error handling goes here
			sk.run_algo = False
			text = f"Kucoin - error on trade for quantity: {quantity} and {precision}, algo stopped, KucoinAPIException {e}"
			Trade_algo.send_text(text, exchange = 'kucoin')
		except MarketOrderException as e:
			# error handling goes here
			sk.run_algo = False
			text = f"Kucoin - error on trade for quantity: {quantity} and {precision}, algo stopped, MarketOrderException {e}"
			Trade_algo.send_text(text, exchange = 'kucoin')
		except Exception as e:
			sk.run_algo = False
			text = f"Kucoin - error on trade for quantity: {quantity} and {precision}, algo stopped, general exception {e}"
			Trade_algo.send_text(text, exchange = 'kucoin')

	else:
		text = f"Kucoin: {currency_name}:fake order {order_type} done for a quantity of {quantity} {currency_name} at price {current_price}"
		Trade_algo.send_text(text, exchange = 'kucoin')
		"""
		if order_type == "Buy":
			sb.current_money_available = max(sb.current_money_available - Currency.current_price * quantity, 0)
			Currency.current_crypto_available = Currency.current_crypto_available + quantity
		elif order_type == "Sell":
			sb.current_money_available = sb.current_money_available + Currency.current_price * quantity
			Currency.current_crypto_available = max(Currency.current_crypto_available - quantity, 0)
		"""

def get_currency_min_notional(Currency):
	info = sk.client.get_symbol_info(Currency.Currency)
	Currency.min_notional = float(info['filters'][3]['minNotional'])
	StepSize = float(info['filters'][2]['stepSize'])
	Currency.precision = int(round(-math.log(StepSize, 10), 0))
	Currency.precision = Currency.precision - 2 #found on internet, doesn't make sense ...
	if Currency.precision < 0:
		Currency.precision = 0
	Currency.qty_reduce_only = round(float(info['filters'][5]['maxQty'])/100, 0)

def get_all_pairs():
	info = sk.client.get_symbols()
	sk.df_all_pairs = pd.DataFrame(info)
	sk.df_all_pairs = sk.df_all_pairs[['baseCurrency','quoteCurrency','symbol','enableTrading','quoteMinSize', 'baseMinSize']]
	sk.df_all_pairs.columns = ['baseAsset','quoteAsset','symbol','status','minNotional', 'stepSize']
	sk.df_all_pairs['status'] = np.where(sk.df_all_pairs.status == True, "TRADING", sk.df_all_pairs.status)


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


def get_all_prices():
	#time.sleep(0.01)
	try:
		kucoin_prices = pd.DataFrame(sk.client.get_ticker()['ticker'])
		sk.all_prices = kucoin_prices
	except requests.exceptions.Timeout:
		text = f"{datetime.now().strftime('%H:%M:%S')} kucoin read price timeout has occured"
		Trade_algo.send_text(text, exchange = 'kucoin')
	except Exception as e:
		text = f"{datetime.now().strftime('%H:%M:%S')} kucoin error has occured: {e}"
		Trade_algo.send_text(text, exchange = 'kucoin')

def prepare_price_list_for_websocket():
	get_all_prices()
	sk.all_prices_websocket = sk.all_prices.copy()
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['averagePrice', 'buy', 'changePrice', 'changeRate', 'high'])
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['takerCoefficient', 'takerFeeRate', 'vol', 'volValue'])
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['low', 'makerCoefficient', 'makerFeeRate', 'sell'])
	sk.all_prices_websocket['lastUpdateTime'] = 0
	sk.all_prices_websocket['period'] = 0
	sk.all_prices_websocket['ksm'] = 0

def fiat_available(Currency = "USDT", Log = False):
	# shall be call first, reset current total
	sk.current_total = 0
	if sk.api_key != None and sk.test == False and Log == True:
		#time.sleep(0.01)
		value = pd.DataFrame(sk.client.get_accounts())
		sk.current_money_available = float(value.loc[(value['currency'] == Currency) & (value['type'] == "trade")]["available"].item())
	sk.current_total = sk.current_money_available
	sk.balance = round(sk.current_total - sk.total_money_available, 2)

def get_money(Currency = "USDT"):
	amount = 'Not available'
	if sk.api_key != None:
		#time.sleep(0.01)
		value = pd.DataFrame(sk.client.get_accounts())
		amount = float(value.loc[(value['currency'] == Currency) & (value['type'] == "trade")]["available"].item())
	return amount

def fetch_current_ticker_price(currency_name, price_list, buy_or_sell):
	price_row = price_list.loc[price_list['symbol'] == currency_name]
	if buy_or_sell == 'buy':
		price = float(price_row["last"].item())
	else:
		price = float(price_row["last"].item())
	return price

def update_time():
	current_time = int(time.time() * 1000)
	for row in tqdm(sk.all_prices_websocket.itertuples()):
		sk.all_prices_websocket.at[row[0], 'period'] = current_time - int(sk.all_prices_websocket.at[row[0], 'lastUpdateTime'])

async def websocket_get_tickers_and_account_balance(loop):

	async def compute(msg):
		"""
		if msg['topic'] == '/market/ticker:BTC-USDT':
			print(f'got ETH-USDT tick:{msg["data"]}')
			print(f'ETH-USDT tick time between {int(time.time() * 1000) - int(msg["data"]["time"])}', flush=True)

		if msg['topic'] == '/market/ticker:MANA-BTC':
			print(f'got MANA-BTC tick:{msg["data"]["price"]}')
			print(f'MANA-BTC tick time between {int(time.time() * 1000) - int(msg["data"]["time"])}', flush=True)
			sk.msg = msg

		elif msg['topic'] == '/market/ticker:all':
			#print(f'got all market snapshot:{msg}')
			#print(f'all tickers tick time between {int(time.time() * 1000) - int(msg["data"]["time"])}', flush=True)
		elif msg['topic'] == '/account/balance':
			print(f'got account balance:{msg["data"]}')
		"""
		#sk.msg = msg
		#update price in price list
		#symbol=msg['topic'].split(':')[1]
		symbol=msg['subject']
		sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'last'] = msg["data"]["price"]
		sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'lastUpdateTime'] = msg["data"]["time"]
		#sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'period'] = int(time.time() * 1000) - int(msg["data"]["time"])
		#sk.all_prices_websocket.loc[sk.all_prices_websocket['lastUpdateTime'] != 0]

	# callback function that receives messages from the socket
	async def handle_evt(msg):
		task = asyncio.create_task(compute(msg))
		await task


	ksm = await KucoinSocketManager.create(loop, sk.client, handle_evt)
	#ksm_private = await KucoinSocketManager.create(loop, sk.client, handle_evt, private=True)

	# Note: try these one at a time, if all are on you will see a lot of output

	# ETH-USDT Market Ticker
	#await ksm.subscribe('/market/ticker:BTC-USDT')
	#await ksm.subscribe('/market/ticker:MANA-BTC')
	# Account balance - must be authenticated
	#await ksm_private.subscribe('/account/balance')
	# All tickers
	await ksm.subscribe('/market/ticker:all')
	"""
	topic = '/market/ticker:'
	for row in tqdm(sk.all_prices_websocket.itertuples()): 
		topic = topic + ',' + str(row[2])
		#print(f'{topic}')
		#sk.all_prices_websocket.at[row[0], 'ksm'] = await KucoinSocketManager.create(loop, sk.client, handle_evt)
		#await sk.all_prices_websocket.at[row[0], 'ksm'].subscribe(topic)
	
	await ksm.subscribe(topic)
	"""

	while True:
		print("sleeping to keep loop open")
		#update_time()
		#current_time = int(time.time() * 1000)
		#sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', 'period'] = current_time - int(sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', 'lastUpdateTime'])
		text = sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']
		#text = sk.all_prices_websocket
		print(f'{text}')
		await asyncio.sleep(5, loop=loop)


def start_websocket():
	# for private topics such as '/account/balance' pass private=True
	loop.run_until_complete(websocket_get_tickers_and_account_balance())

if __name__ == "__main__":
   main()

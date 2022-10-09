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
from urllib3.exceptions import InsecureRequestWarning




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
		kucoin_prices = kucoin_prices.rename(columns={"last": "price"})
		sk.all_prices = kucoin_prices
		#print(f'{sk.all_prices}')
	except requests.exceptions.Timeout:
		text = f"{datetime.now().strftime('%H:%M:%S')} kucoin read price timeout has occured"
		Trade_algo.send_text(text, exchange = 'kucoin')
	except Exception as e:
		text = f"{datetime.now().strftime('%H:%M:%S')} kucoin error has occured: {e}"
		Trade_algo.send_text(text, exchange = 'kucoin')

def prepare_price_list_for_websocket():
	#sk.all_prices_websocket = sk.arbitrage_opportunity.copy()
	sk.all_prices_websocket = pd.read_json('Arbitrage_oppotunities.json')
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['time'])
	sk.df_all_pairs_arbitrage = sk.all_prices_websocket.copy()
	sk.df_all_pairs_arbitrage.insert(0, 'baseAsset', sk.all_prices_websocket['symbol'].str.split('-',expand = True)[0])
	sk.df_all_pairs_arbitrage.insert(1, 'quoteAsset', sk.all_prices_websocket['symbol'].str.split('-',expand = True)[1])
	sk.df_all_pairs_arbitrage['status'] = 'TRADING'

	sk.all_prices_websocket['price'] = 0
	sk.all_prices_websocket['symbolName'] = 0
	sk.all_prices_websocket['current_quantity'] = 0
	sk.all_prices_websocket['lastUpdateTime'] = 0
	sk.all_prices_websocket['period'] = 0
	sk.all_prices_websocket['index'] = 0
	sk.all_prices_websocket['_index_running'] = 0


	"""
	get_all_prices()
	sk.all_prices_websocket = sk.all_prices.copy()
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['averagePrice', 'buy', 'changePrice', 'changeRate', 'high'])
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['takerCoefficient', 'takerFeeRate', 'vol', 'volValue'])
	sk.all_prices_websocket = sk.all_prices_websocket.drop(columns=['low', 'makerCoefficient', 'makerFeeRate', 'sell'])
	sk.all_prices_websocket['lastUpdateTime'] = 0
	sk.all_prices_websocket['period'] = 0
	sk.all_prices_websocket['index'] = 0
	"""

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
	amount = None
	if sk.api_key != None:
		#time.sleep(0.01)
		try:
			value = pd.DataFrame(sk.client.get_accounts())
			amount = float(value.loc[(value['currency'] == Currency) & (value['type'] == "trade")]["available"].item())
		except Exception as e:
			if sk.do_real_order == True:
				text = f"{datetime.now().strftime('%H:%M:%S')} kucoin error has occured: {e}"
				Trade_algo.send_text(text, exchange = 'kucoin')

				#else do nothing this error can happen when do order is False cause trade has not been set and amount is Null

	return amount

def get_quantity_websocket(symbol = "USDT"):
	amount = sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'current_quantity']
	return amount


def fetch_current_ticker_price(currency_name, price_list, buy_or_sell):
	price = float(price_list.loc[price_list['symbol'] == currency_name]["price"].item())
	"""
	price_row = price_list.loc[price_list['symbol'] == currency_name]
	#print(f'{price_row}')
	try:
		if price_row.empty:
			price = None
		elif buy_or_sell == 'buy':
			price = float(price_row["price"].item())
		else:
			price = float(price_row["price"].item())
	except Exception as e:
		price = None
	"""

	if price == 0:
		#price = float(1) #avoid zero division but no error handling
		price = None
	#print(f'{price}')
	
	return price

def update_time():
	current_time = int(time.time() * 1000)
	for row in tqdm(sk.all_prices_websocket.itertuples()):
		sk.all_prices_websocket.at[row[0], 'period'] = current_time - int(sk.all_prices_websocket.at[row[0], 'lastUpdateTime'])

def check_if_websocket_is_running():
	#check BTC
	#print(f"websocket btc is {sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']}")
	if sk.run_algo and int(sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', 'index']) > 10:

		current_period = int(time.time() * 1000) - int(sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', 'lastUpdateTime'])
		#print(f"period is {current_period} and websocket btc is {sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']}")

		#websocket api is supposed to be 100ms
		if current_period > 5000: #1s
			"""
			index = int(sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', 'index'])
			index_running = int(sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', '_index_running'])

			if index > index_running:
				#means everything ok
				sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', '_index_running'] = index

			if index == index_running:
				sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT', '_index_running'] = index + 1
			
			elif index < index_running:
			"""
			#sk.run_algo = False
			#text = f"Kucoin: error on websocket running,index are {index} and {index_running} and run algo is: {sk.run_algo}"
			text = f"Kucoin: error on websocket running, period is {current_period} and run algo is: {sk.run_algo}"

			Trade_algo.send_text(text, exchange = 'kucoin')

async def websocket_get_tickers_and_account_balance(init_time):

	async def compute(msg):

		sk.msg = msg
		#print(f'{sk.msg}')

		if msg['topic'] == '/spot/tradeFills':
			print(f'{sk.msg}')
			symbol=msg["data"]["symbol"]

			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'current_quantity'] = float(msg["data"]["size"])
			size = sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'current_quantity']
			text = f"Kucoin: {symbol}: quantity executed is: {size}"
			Trade_algo.send_text(text, exchange = 'kucoin')
		elif msg['topic'].split(':')[0] == '/market/ticker':
			#update price in price list
			symbol=msg['topic'].split(':')[1]
			#symbol=msg['subject']
			#print(f'{symbol}')
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'price'] = msg["data"]["price"]
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'lastUpdateTime'] = msg["data"]["time"]
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'index'] += 1
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'period'] = int(time.time() * 1000) - int(msg["data"]["time"])
			print(f"websocket btc is {sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']}")

		update_data_coming_from_other_process("send")

	# callback function that receives messages from the socket
	async def handle_evt(msg):
		task = asyncio.create_task(compute(msg))
		await task

	
	print("start ksm")
	loop = asyncio.get_event_loop()
	ksm_private = await KucoinSocketManager.create(loop, sk.client, handle_evt, private = True)
	ksm = await KucoinSocketManager.create(loop, sk.client, handle_evt)
	print(f'{ksm_private}')
	print(f'{ksm}')

	await asyncio.sleep(init_time)

	topic_private = '/spotMarket/tradeOrders'
	topic = '/market/ticker:'

	for row in tqdm(sk.all_prices_websocket.itertuples()):
		#print(f'{index}')
		if row[0] == 0:
			topic = topic + str(row[1])
		elif row[0] > 0:
			topic = topic + ',' + str(row[1])
	print(f'{topic}')

	
	await ksm_private.subscribe(topic_private)
	await ksm.subscribe(topic)

def update_data_coming_from_other_process(function):
	
	if function == "send":
		sk.pipe_send_arbitrage.send(sk.msg)
		#sk.pipe_send_arbitrage.send(sk.all_prices_websocket)
		#sk.pipe_send_discord.send(sk.all_prices_websocket)
	if function == "arbitrage":
		while sk.pipe_recv_arbitrage.poll():
			#sk.all_prices_websocket = sk.pipe_recv_arbitrage.recv()
			msg = sk.pipe_recv_arbitrage.recv()
			symbol=msg['topic'].split(':')[1]
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'price'] = msg["data"]["price"]
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'lastUpdateTime'] = msg["data"]["time"]
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'index'] += 1
			sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == symbol, 'period'] = int(time.time() * 1000) - int(msg["data"]["time"])
			
	elif function == "discord":
		while sk.pipe_recv_discord.poll():
			sk.all_prices_websocket = sk.pipe_recv_discord.recv()


if __name__ == "__main__":
   main()

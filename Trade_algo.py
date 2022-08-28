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
import pandas_ta as ta
import Binance_trade
import Kucoin_trade
	

def update_price(Currency, date = 'None'):

	Currency.current_price = Currency.price[Currency.Currency].price.iloc[-1]

	#check if price is the same
	if Currency.price['price_stuck_algo'] > 5:
		Currency.price['error'] = True
		Currency.price['price_stuck_algo'] = 0
	elif Currency.price['old_price_algo'] == Currency.current_price:
		Currency.price['price_stuck'] = Currency.price['price_stuck'] + 1
	else:
		Currency.price['price_stuck'] = 0

	Currency.price['old_price_algo'] = Currency.current_price

def fetch_price_exchange(exchange, currency_name, price_list, buy_or_sell):
	if exchange == 'binance':
		price = Binance_trade.fetch_current_ticker_price(currency_name, price_list)
	elif exchange == 'kucoin':
		price = Kucoin_trade.fetch_current_ticker_price(currency_name, price_list, buy_or_sell)
	else:
		print(f"fetch_price_exchange: wrong exchange name")
		price = 'None'

	return price

def send_text(text, exchange):
	print(text)
	logging.critical(text)
	if exchange == 'binance':
		if sb.Last_info_to_send == "":
			sb.Last_info_to_send = text
		else:
			sb.Last_info_to_send = sb.Last_info_to_send + """\n""" + text
	elif exchange == 'kucoin':
		if sk.Last_info_to_send == "":
			sk.Last_info_to_send = text
		else:
			sk.Last_info_to_send = sk.Last_info_to_send + """\n""" + text
	else:
		print(f"send_text: wrong exchange name")
			

def fetch_amount_exchange(currency, exchange):
	if exchange == 'binance':
		amount = Binance_trade.get_money(Currency = currency)
	elif exchange == 'kucoin':
		amount = Kucoin_trade.get_money(Currency = currency)
	else:
		print(f"fetch_amount_exchange: wrong exchange name")
		amount = 'None'

	return amount

def fetch_amount_exchange_order(scrip, exchange, order):
	if exchange == 'binance':
		scrip_splitted = scrip.split("/")
	elif exchange == 'kucoin':
		scrip_splitted = scrip.split("-")
	else:
		print(f"fetch_amount_exchange: wrong exchange name")
		amount = 'None'
	
	if order == 'buy':
		amount = fetch_amount_exchange(currency = scrip_splitted[1], exchange = exchange)
	elif order == "sell":
		amount = fetch_amount_exchange(currency = scrip_splitted[0], exchange = exchange)
	else:
		print(f"fetch_amount_exchange: wrong order name")
		amount = 'None'

	return amount

def calculate_amount(amount_exchange, amount_calculated):
	if amount_exchange == None:
		amount = amount_calculated
	else:
		amount = amount_exchange

	return amount

if __name__ == "__main__":
   main()

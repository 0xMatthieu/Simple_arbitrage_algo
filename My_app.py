#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""

import os
from dotenv import load_dotenv
import asyncio
from threading import Thread
from discord.ext import tasks
import settings_binance as sb
from datetime import datetime
import settings_binance as sb
import settings_kucoin as sk
import Binance_trade
import Kucoin_trade
import Main_Arbitrage
import time
import concurrent.futures  
import Trade_algo
import multiprocessing as mp                                                                                
try:
	import psutil
except:
	pass


import ctypes
import numpy as np


def run_app():

	import streamlit as st
	
	print(f"start streamlit app")
	st.write("""
		my App
	""")

	Trade_algo.update_process_data('kucoin', 'discord')
	if sb.Last_info_to_send != "":
		st.write(sb.Last_info_to_send)
		sb.Last_info_to_send = ""
	if sk.Last_info_to_send != "":
		st.write(sk.Last_info_to_send)
		sk.Last_info_to_send = ""

def update_money():
	#sb.init()
	#sk.init()
	Binance_usdt = Binance_trade.get_money(Currency = "USDT")
	Binance_busd = Binance_trade.get_money(Currency = "BUSD")
	Kucoin_usdt = Kucoin_trade.get_money(Currency = "USDT")
	message = (f"Binance: money is {Binance_usdt} USDT and {Binance_busd} BUSD. Kucoin: money is {Kucoin_usdt} USDT")
	return message

def kucoin_value(text):
	Trade_algo.update_process_data('kucoin', 'arbitrage')
	if text == 'btc':
		message = sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']
	elif text == 'all':
		message = sk.all_prices_websocket
	elif text == 'list':
		message = sk.arbitrage_opportunity
	return message

def run_asyncio_functions():
	loop = asyncio.new_event_loop()
	print(f'get loop {loop}')	
	kucoin_task = loop.create_task(Kucoin_trade.websocket_get_tickers_and_account_balance(0))
	loop.run_forever()


def update_list_arbitrage():
	#time.sleep(2)
	print('run async arbitrage')
	while True:
		Main_Arbitrage.run('kucoin','get_list')

def run_arbitrage(num_procs = 2):
	while True:
		#print('run async arbitrage')
		Main_Arbitrage.run('kucoin','do_arbitrage', num_procs)


def app_arbitrage_run():

	sb.init()
	sk.init()

	try:
		num_procs = psutil.cpu_count(logical=True)
	except:
		num_procs = 4

	print(f"num_procs is {num_procs}")

	Main_Arbitrage.init('kucoin','get_list')


	p1 = mp.Process(target=run_arbitrage, args=(num_procs,)).start()
	p2 = mp.Process(target=run_app).start()
	#p3 = mp.Process(target=run_asyncio_functions).start()
	p4 = mp.Process(target=update_list_arbitrage).start()

	#run_app()
	run_asyncio_functions()
	
if __name__ == "__main__":
	app_arbitrage_run()





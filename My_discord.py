#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 14:11:22 2020

@author: matthieu
"""

import os
from dotenv import load_dotenv
import discord
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


discord_thread = Thread()
arbitrage_thread_kucoin_list = Thread()
arbitrage_thread_kucoin_arbitrage = Thread()
client = discord.Client()
load_dotenv(dotenv_path=".env")
channel_id = int(os.environ.get('channel_id'))


@tasks.loop(seconds=1)
async def update_discord():
	channel = client.get_channel(channel_id)
	if sb.Last_info_to_send != "":
		await channel.send(sb.Last_info_to_send)
		sb.Last_info_to_send = ""
	if sk.Last_info_to_send != "":
		await channel.send(sk.Last_info_to_send)
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
	if text == 'btc':
		message = sk.all_prices_websocket.loc[sk.all_prices_websocket['symbol'] == 'BTC-USDT']
	elif text == 'all':
		message = sk.all_prices_websocket
	elif text == 'list':
		message = sk.arbitrage_opportunity
	return message

@client.event
async def on_ready():
	print('We have logged in as {0.user}'.format(client))
	update_discord.start()
	message_to_send = update_money()
	channel = client.get_channel(channel_id)
	await channel.send(message_to_send)
	

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith('channel'):
		await message.channel.send(message.channel.id)

	if message.content.startswith('money'):
		message_to_send = update_money()
		await message.channel.send(message_to_send)

	if message.content.startswith('btc'):
		message_to_send = kucoin_value('btc')
		await message.channel.send(message_to_send)

	if message.content.startswith('all'):
		message_to_send = kucoin_value('all')
		await message.channel.send(message_to_send)

	if message.content.startswith('list'):
		message_to_send = kucoin_value('list')
		await message.channel.send(message_to_send)

	if message.content.startswith('exception'):
		raise Exception('an error occured')

	if message.content.startswith('help'):
		await message.channel.send(f"command are : channel - money - order type - change order - exception")

	if message.content.startswith('change order'):
		sb.do_real_order != sb.do_real_order
		await message.channel.send(f"order type is {sb.do_real_order}. False means fake, True means real ")

	if message.content.startswith('order type'):
		await message.channel.send(f"order type is {sb.do_real_order}. False means fake, True means real ")


def discord_arbitrage_run():

	sb.init()
	sk.init()
	load_dotenv(dotenv_path=".env")
	discord_bot = os.environ.get('discord_bot')
	
	print('start thread kucoin list')
	arbitrage_thread_binance = Thread(target=Main_Arbitrage.main, args=('kucoin','get_list',))
	arbitrage_thread_binance.name = 'kucoin thread list'
	arbitrage_thread_binance.start()
	
	print('start thread kucoin arbitrage')	
	arbitrage_thread_kucoin = Thread(target=Main_Arbitrage.main, args=('kucoin','do_arbitrage',), daemon=True)
	arbitrage_thread_kucoin.name = 'kucoin thread arbitrage'
	arbitrage_thread_kucoin.start()

	print('start thread discord')
	loop = asyncio.get_event_loop()
	loop.create_task(Kucoin_trade.websocket_get_tickers_and_account_balance(10))
	loop.create_task(client.start(discord_bot))
	discord_thread = Thread(target=loop.run_forever)
	discord_thread.name = 'discord thread'
	discord_thread.start()

	arbitrage_thread_binance.join()
	arbitrage_thread_kucoin.join()
	discord_thread.join()



if __name__ == "__main__":
	discord_arbitrage_run()




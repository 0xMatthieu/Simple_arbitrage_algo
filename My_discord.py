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
arbitrage_thread_binance = Thread()
arbitrage_thread_kucoin = Thread()
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

	if message.content.startswith('exception'):
		raise Exception('an error occured')

	if message.content.startswith('alive'):
		await message.channel.send(f"arbitrage thread is {arbitrage_thread_binance.is_alive()}")
		await message.channel.send(f"arbitrage thread is {arbitrage_thread_kucoin.is_alive()}")

	if message.content.startswith('help'):
		await message.channel.send(f"command are : channel - money - order type - change order - exception")

	if message.content.startswith('change order'):
		sb.do_real_order != sb.do_real_order
		await message.channel.send(f"order type is {sb.do_real_order}. False means fake, True means real ")

	if message.content.startswith('order type'):
		await message.channel.send(f"order type is {sb.do_real_order}. False means fake, True means real ")



def discord_arbitrage_run():
	global discord_thread, arbitrage_thread_binance, arbitrage_thread_kucoin
	"""
	print('start thread 1')
	loop = asyncio.get_event_loop()
	loop.create_task(client.start('OTg2NTQ1MjcwNzk4MDQxMTE4.GvZsfg.y8buGZv_T-F1JcqBcajk5wedlR_XAUXMyPKkb8'))
	discord_thread = Thread(target=loop.run_forever).start()
	print('start thread 2')
	arbitrage_thread = Thread(target=Main_Arbitrage.main()).start()
	"""
	load_dotenv(dotenv_path=".env")

	time.sleep(10)

	print('start thread binance')
	arbitrage_thread_binance = Thread(target=Main_Arbitrage.main, args=('binance',))
	arbitrage_thread_binance.name = 'binance thead'
	arbitrage_thread_binance.start()

	print('start thread kucoin')
	arbitrage_thread_kucoin = Thread(target=Main_Arbitrage.main, args=('kucoin',))
	arbitrage_thread_kucoin.name = 'kucoin thead'
	arbitrage_thread_kucoin.start()

	print('start thread discord')
	discord_bot = os.environ.get('discord_bot')
	loop = asyncio.get_event_loop()
	loop.create_task(client.start(discord_bot))
	discord_thread = Thread(target=loop.run_forever)
	discord_thread.name = 'binance thead'
	discord_thread.start()

	
	"""
	while True:
		time.sleep(10)

		if arbitrage_thread_binance.is_alive() == False:
			print(f"{datetime.now().strftime('%H:%M:%S')} arbitrage thread is dead, restart")
			sb.Last_info_to_send = f"{datetime.now().strftime('%H:%M:%S')} arbitrage thread is dead, restart"
			print('start thread binance')
			arbitrage_thread_binance = Thread(target=Main_Arbitrage.main, args=('binance',)).start()
			#time.sleep(5)

		if arbitrage_thread_kucoin.is_alive() == False:
			print(f"{datetime.now().strftime('%H:%M:%S')} arbitrage thread is dead, restart")
			sb.Last_info_to_send = f"{datetime.now().strftime('%H:%M:%S')} arbitrage thread kucoin is dead, restart"
			print('start thread kucoin')
			arbitrage_thread_kucoin = Thread(target=Main_Arbitrage.main, args=('kucoin',)).start()
			#time.sleep(5)

		if discord_thread.is_alive() == False:
			print(f"{datetime.now().strftime('%H:%M:%S')} discord thread is dead, restart")
			print('start thread discord')
			loop = asyncio.get_event_loop()
			loop.create_task(client.start('OTg2NTQ1MjcwNzk4MDQxMTE4.GvZsfg.y8buGZv_T-F1JcqBcajk5wedlR_XAUXMyPKkb8'))
			discord_thread = Thread(target=loop.run_forever).start()
			#time.sleep(5)
	"""

if __name__ == "__main__":
	discord_arbitrage_run()




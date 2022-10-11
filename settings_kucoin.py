
import os
from dotenv import load_dotenv
import pandas as pd 
from kucoin.client import Client
import numpy as np
import multiprocessing as mp




def init():
    global Currency_fiat, client, do_real_order, \
    total_money_available, current_money_available, current_total, balance, order_done_current_cycle, \
    api_key, api_secret, test, df_all_pairs, df_all_currencies, df_unique_currencies, dict_all_combinations, \
    fiat_list, crypto_list, Index, Last_info_to_send, run_algo, msg, all_prices, all_prices_websocket, arbitrage_opportunity, \
    df_all_pairs_arbitrage, df_all_combinations_arbitrage, dict_all_combinations_arbitrage, df_unique_currencies_arbitrage, \
    pipe_recv_arbitrage, pipe_send_arbitrage, pipe_recv_discord, pipe_send_discord, start, index

    #general
    do_real_order = False
    test = False
    Currency_fiat = 'EUR'
    total_money_available = 0
    current_money_available = 0
    current_total = 0
    balance = 0
    order_done_current_cycle = False
    df_all_pairs = pd.DataFrame()
    df_all_currencies = pd.DataFrame()
    df_all_combinations = pd.DataFrame()
    df_unique_currencies = pd.DataFrame()
    all_prices = pd.DataFrame()
    all_prices_websocket = pd.DataFrame()
    dict_all_combinations = 0
    df_all_pairs_arbitrage = pd.DataFrame()
    df_all_combinations_arbitrage = pd.DataFrame()
    dict_all_combinations_arbitrage = 0
    df_unique_currencies_arbitrage = pd.DataFrame()
    arbitrage_opportunity = pd.DataFrame(columns=['time', 'symbol'])
    fiat_list = ["GBP", "TRY", "KZP", "AUD", "BRL", "PEN", "RUB", "UAH", "UGX", "PHP", "USD" ]
    crypto_list = ["BCC", "MCO", "VEN", "XZC" ]
    Index = 0
    Last_info_to_send = ""
    run_algo = True
    msg = 0
    start = 0
    index = 0

    pipe_recv_arbitrage, pipe_send_arbitrage = mp.Pipe(duplex = False)
    pipe_recv_discord, pipe_send_discord = mp.Pipe(duplex = False)



    # init
    load_dotenv(dotenv_path=".env")
    api_key = os.environ.get('api_key_kucoin')
    api_secret = os.environ.get('api_secret_kucoin')
    api_passphrase = os.environ.get('api_passphrase_kucoin')
    client = Client(api_key, api_secret, api_passphrase)



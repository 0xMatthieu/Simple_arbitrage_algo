
import os
from dotenv import load_dotenv
import pandas as pd 
from kucoin.client import Client
import numpy as np




def init():
    global Currency_fiat, client, do_real_order, \
    total_money_available, current_money_available, current_total, balance, order_done_current_cycle, \
    api_key, api_secret, test, df_all_pairs, df_all_currencies, df_unique_currencies, dict_all_combinations, \
    fiat_list, crypto_list, Index, Last_info_to_send, run_algo, msg, all_prices, all_prices_websocket

    #general
    do_real_order = True
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
    fiat_list = ["GBP", "TRY", "KZP", "AUD", "BRL", "PEN", "RUB", "UAH", "UGX", "PHP", "USD" ]
    crypto_list = ["BCC", "MCO", "VEN", "XZC" ]
    Index = 0
    Last_info_to_send = ""
    run_algo = True
    msg = 0



    # init
    load_dotenv(dotenv_path=".env")
    api_key = os.environ.get('api_key_kucoin')
    api_secret = os.environ.get('api_secret_kucoin')
    api_passphrase = os.environ.get('api_passphrase_kucoin')
    client = Client(api_key, api_secret, api_passphrase)



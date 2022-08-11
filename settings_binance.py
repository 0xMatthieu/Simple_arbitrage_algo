
import os
from dotenv import load_dotenv
import pandas as pd 
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance import ThreadedWebsocketManager, Client, ThreadedDepthCacheManager
import numpy as np

class Currency:
    "currency class"

    def __init__(self, Currency, Currency_crypto):
        self.Currency = Currency
        self.Currency_crypto = Currency_crypto
        self.price = {Currency: pd.DataFrame(columns=['date', 'price']), 'error':False, 'old_price':0, 'price_stuck':0, 'price_stuck_algo':0, 'old_price_algo':0}
        self.order_book = {'book': pd.DataFrame(columns=['bids', 'quantity']), 'error':False, 'old_book':0}
        self.current_crypto_available = 0
        self.current_price = 0
        self.last_price = 0
        self.min_notional = 0
        self.precision = 0
        self.twm = 0 # init in binance trade ThreadedWebsocketManager(api_key=api_key, api_secret=api_secret)
        self.dcm = 0
        self.percentage = 1

        self.init = True

        #arbitrage 
        self.arg_max_element = 5
        self.top_bids = 0 
        self.top_asks = 0
        self.update_time = 0
        self.depth_message = 0



def init():
    global Currency_fiat, client, do_real_order, \
    total_money_available, current_money_available, current_total, balance, order_done_current_cycle, \
    api_key, api_secret, test, df_all_pairs, df_all_currencies, df_unique_currencies, dict_all_combinations, \
    fiat_list, crypto_list, Index, Last_info_to_send, run_algo

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
    dict_all_combinations = 0
    fiat_list = ["GBP", "TRY", "KZP", "AUD", "BRL", "PEN", "RUB", "UAH", "UGX", "PHP", "USD" ]
    crypto_list = ["BCC", "MCO", "VEN", "XZC" ]
    Index = 0
    Last_info_to_send = ""
    run_algo = True


    # init
    load_dotenv(dotenv_path=".env")
    api_key = os.environ.get('api_key_binance')
    api_secret = os.environ.get('api_secret_binance')
    client = Client(api_key, api_secret)



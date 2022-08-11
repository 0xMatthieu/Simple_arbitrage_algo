scp -r /Users/matthieu/Documents/Python/Binance/220605_Arbitrage matthieu@192.168.1.19:/home/matthieu/python/Binance/

python -m pip install discord
python -m pip install python-kucoin
python -m pip install python-dotenv

lxterminal -e "cd /home/matthieu/python/Binance/220605_Arbitrage/ ; python Main_Arbitrage.py"

source : https://medium.com/geekculture/automated-triangular-arbitrage-of-cryptos-in-4-steps-a678f7b01ce7

220605  - first version

220702	- add kucoin exchange



matthieu@ubuntu:~/python/Binance/220605_Arbitrage$ python -i My_discord.py
start thread binance
start thread kucoin
start thread discord
>>> We have logged in as My_bot#7422
Start software kucoin -08:11:34
Start software binance -08:11:44
>>> Exception in thread Thread-4:
Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 387, in _make_request
    six.raise_from(e, None)
  File "<string>", line 3, in raise_from
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 383, in _make_request
    httplib_response = conn.getresponse()
  File "/usr/lib/python3.7/http/client.py", line 1348, in getresponse
    response.begin()
  File "/usr/lib/python3.7/http/client.py", line 315, in begin
    version, status, reason = self._read_status()
  File "/usr/lib/python3.7/http/client.py", line 276, in _read_status
    line = str(self.fp.readline(_MAXLINE + 1), "iso-8859-1")
  File "/usr/lib/python3.7/socket.py", line 589, in readinto
    return self._sock.recv_into(b)
  File "/usr/lib/python3.7/ssl.py", line 1071, in recv_into
    return self.read(nbytes, buffer)
  File "/usr/lib/python3.7/ssl.py", line 929, in read
    return self._sslobj.read(len, buffer)
socket.timeout: The read operation timed out

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 440, in send
    timeout=timeout
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 639, in urlopen
    _stacktrace=sys.exc_info()[2])
  File "/usr/lib/python3/dist-packages/urllib3/util/retry.py", line 367, in increment
    raise six.reraise(type(error), error, _stacktrace)
  File "/usr/lib/python3/dist-packages/six.py", line 693, in reraise
    raise value
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 601, in urlopen
    chunked=chunked)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 389, in _make_request
    self._raise_timeout(err=e, url=url, timeout_value=read_timeout)
  File "/usr/lib/python3/dist-packages/urllib3/connectionpool.py", line 309, in _raise_timeout
    raise ReadTimeoutError(self, url, "Read timed out. (read timeout=%s)" % timeout_value)
urllib3.exceptions.ReadTimeoutError: HTTPSConnectionPool(host='api.binance.com', port=443): Read timed out. (read timeout=10)

During handling of the above exception, another exception occurred:

Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "/home/matthieu/python/Binance/220605_Arbitrage/Main_Arbitrage.py", line 125, in main
    Binance_trade.get_all_prices()
  File "/home/matthieu/python/Binance/220605_Arbitrage/Binance_trade.py", line 170, in get_all_prices
    sb.all_prices = pd.DataFrame(sb.client.get_all_tickers())
  File "/home/matthieu/.local/lib/python3.7/site-packages/binance/client.py", line 571, in get_all_tickers
    return self._get('ticker/price', version=self.PRIVATE_API_VERSION)
  File "/home/matthieu/.local/lib/python3.7/site-packages/binance/client.py", line 371, in _get
    return self._request_api('get', path, signed, version, **kwargs)
  File "/home/matthieu/.local/lib/python3.7/site-packages/binance/client.py", line 334, in _request_api
    return self._request(method, uri, signed, **kwargs)
  File "/home/matthieu/.local/lib/python3.7/site-packages/binance/client.py", line 314, in _request
    self.response = getattr(self.session, method)(uri, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 533, in get
    return self.request('GET', url, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 520, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python3/dist-packages/requests/sessions.py", line 630, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python3/dist-packages/requests/adapters.py", line 521, in send
    raise ReadTimeout(e, request=request)
requests.exceptions.ReadTimeout: HTTPSConnectionPool(host='api.binance.com', port=443): Read timed out. (read timeout=10)

02:35:03 kucoin error has occured: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
06:19:08 kucoin error has occured: ('Connection aborted.', ConnectionResetError(104, 'Connection reset by peer'))
03:31:20 kucoin read price timeout has occured
11:14:00 kucoin read price timeout has occured
Exception in thread Thread-5:
Traceback (most recent call last):
  File "/usr/lib/python3.7/threading.py", line 926, in _bootstrap_inner
    self.run()
  File "/usr/lib/python3.7/threading.py", line 870, in run
    self._target(*self._args, **self._kwargs)
  File "/home/matthieu/python/Binance/220605_Arbitrage/Main_Arbitrage.py", line 179, in main
    BROKERAGE_PER_TRANSACTION_PERCENT, MIN_PROFIT_DOLLARS, exchange, sk.all_prices)
  File "/home/matthieu/python/Binance/220605_Arbitrage/Arbitrage.py", line 165, in perform_triangular_arbitrage
    final_price, scrip_prices = check_buy_sell_sell(scrip1, scrip2, scrip3, price_list, initial_investment, exchange)
  File "/home/matthieu/python/Binance/220605_Arbitrage/Arbitrage.py", line 94, in check_buy_sell_sell
    current_price1 = Trade_algo.fetch_price_exchange(exchange, scrip1, price_list, 'buy')
  File "/home/matthieu/python/Binance/220605_Arbitrage/Trade_algo.py", line 37, in fetch_price_exchange
    Kucoin_trade.fetch_current_ticker_price(currency_name, price_list, buy_or_sell)
  File "/home/matthieu/python/Binance/220605_Arbitrage/Kucoin_trade.py", line 127, in fetch_current_ticker_price
    price = float(price_row["buy"].item())
  File "/home/matthieu/.local/lib/python3.7/site-packages/pandas/core/base.py", line 660, in item
    raise ValueError("can only convert an array of size 1 to a Python scalar")
ValueError: can only convert an array of size 1 to a Python scalar

>>> 

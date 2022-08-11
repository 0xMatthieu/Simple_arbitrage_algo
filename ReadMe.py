scp -r /Users/matthieu/Documents/Python/Binance/220605_Arbitrage matthieu@192.168.1.19:/home/matthieu/python/Binance/

python -m pip install discord
python -m pip install python-kucoin
python -m pip install python-dotenv

lxterminal -e "cd /home/matthieu/python/Binance/220605_Arbitrage/ ; python Main_Arbitrage.py"

source : https://medium.com/geekculture/automated-triangular-arbitrage-of-cryptos-in-4-steps-a678f7b01ce7

220605  - first version

220702	- add kucoin exchange

git help
git rm .env --cached
git commit -m "Stopped tracking .env File"
git push -u origin main

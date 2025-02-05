# Crypto_arbitrage_bot

## Overview
This repository implements a crypto arbitrage bot designed to run as fast as possible using multithreading and pipes to parallelize data flow between various components. The goal is to leverage concurrent execution to handle rapid data streams and execute trading decisions swiftly.

## Repository Structure
- Arbitrage.py: Contains core functions for calculating crypto arbitrage opportunities, including functions to analyze combinations and perform trades.
- Arbitrage_oppotunities.json: Stores arbitrage opportunities detected by the system.
- Binance_trade.py: Implements trading functions and data retrieval for the Binance exchange.
- Kucoin_trade.py: Implements trading functions including market order execution and websocket stream handling for the Kucoin exchange. Also manages asynchronous ticker and account balance updates.
- Main_Arbitrage.py: Coordinates REST API and websocket based trading strategies, initiating arbitrage operations.
- My_discord.py: Implements a Discord bot that notifies trading events and integrates the arbitrage execution.
- Trade_algo.py: Provides algorithms for price fetching, amount calculations, and trade instruction dispatching.
- settings_binance.py & settings_kucoin.py: Contain configuration settings for their respective exchanges.
- .env.example, .gitignore, LICENSE: Contain environment settings, repository configuration, and legal information.

## How to Start
Run the following command to start the Discord bot interface, which in turn integrates the arbitrage functionality:
  python My_discord.py

## Detailed Explanation
The software is structured to separate trading logic from IO operations. It uses multithreading to execute tasks in parallel and pipes to efficiently pass data between processes. This design minimizes delays from REST API responses and websocket streams, enabling rapid decision-making and execution of arbitrage trades.


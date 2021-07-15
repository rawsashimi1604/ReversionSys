# Mean Reversion Stock Trading System, ReversionSys
*Made by rawsashimi1604*

### Introduction
Hey everyone! :wave: This is a stock trading system that I developed, using a trading software called **Amibroker, Python and TWS Interactive Brokers API**.

Huge thanks to *erdiwit* for creating *ib_insync* module to make programming this much more linear!

![STATISTICS](https://user-images.githubusercontent.com/75880261/108598516-f8d08280-73c8-11eb-8cd6-7eea9db620e5.PNG)

### Required modules
- talib library (use whl to install, file in package)
- pandas
- numpy
- yfinance
- ib_insync
- pprint

### Installation
- Install TWS Workstation
- Install required modules
- Run TWS Workstation
- Configure TWS API Settings (ip, socket, enable)
- Run python code
- Leave TWS on
- Use main.py to run get_trade_list or run_bot

### Tips and Tricks
- Update S&P 500 Components every month to account for changes in index.
- Get list of trades everyday before the market opens.

### How does the trading system work?
#### Research material and background
For starters, I was looking into some stock trading strategies and methods that have proved profitable so far. I came across this book, **Short Term Trading Strategies that Work by Larry Connors.**

Larry described some useful pointers backed by statistics such as:
- Buying pullbacks, and using the Relative Strength Index (RSI) to detect them,
- Buy stocks in an uptrend,
- Using intra-day pullbacks to get a better entry price.

As such, I used some of his parameters and tested it out on a backtesting software, **Amibroker.**

#### Trading System
Here were the **parameters** I used for my trading system.

- *Moving Average Period* = 100
- *RSI Period* = 2
- *RSI Buy Signal* = 5
- *RSI Exit Period* = 5
- *RSI Exit Signal* = 40
- *Max Positions to Hold* = 3
- *Limit Order* = 1.5%

For the stock universe, I used only the **S&P500 Index Stocks.**

As for position sizing, each time a position was available, it took up 33% of my portfolio.

As for the ranking system, I chose stocks that ranked the highest in the *Rate of Change(ROC) = 100* and *ROC > 0* parameter. This is to choose stocks with high relative strength only.

#### Example of the trading system (using PineScript from Tradingview)
> *Here is an entry example from TradingView*
![AAPL TRADING EXAMPLE](https://user-images.githubusercontent.com/75880261/108593823-0b3ec200-73b1-11eb-8c3c-6a74a165d747.png)

> *Here is an exit example*
![AAPL TRADING EXAMPLE (1)](https://user-images.githubusercontent.com/75880261/108593816-011cc380-73b1-11eb-90a3-80d80a30d6af.png)

> For more information, you can refer to the amibroker AFL code.

### Getting a trade list everyday.
To get the list of trades today, we use the function *get_trade_list*.
```python
def get_trade_list(file_type, components_path=r"C:\\Users\\rawsashimi1604\\VisualStudio\\Reversion_Sys\\ReversionSys\\S&P500 Components.csv", export_path="C:\\Users\\rawsashimi1604\\VisualStudio\\Reversion_Sys\\ReversionSys"):
  # some code
  returns None
```
Parameters:
  - file_type : *str*
    - Use either "csv" or "txt"
      - Specifies what file_type to receive today's list of trades in.
  - components_path : *str*
    - Specifies where to find list of tickers to trade in. (S&P500 Component List)
  - export_path : *str*
    - Specifies where to export today's list of trades.

Returns:
  - None

To run the bot we use the function *run_bot*.
```python
def run_bot(path = "C:\\Users\\rawsashimi1604\\VisualStudio\\Reversion_Sys\\ReversionSys\\2021-01-25 Reversion Trades.csv", market_open_time = "22:30:05", ip='127.0.0.1', socket=7497, clientId=1):
  # some code
  returns None
```
Parameters:
  - path : *str*
    - Specifies where list of trades csv is.
  - market_open_time : *str*
    - Specifies what time in local time the stock market opens. Default is *"22:30:05"*.
  - ip : *str*
    - Specifies TWS IP Address Settings. Default is *"127.0.0.1"*.
  - socket : *int*
    - Specifies TWS Socket Settings. Default is *7497*.
  - clientId : *int*
    - Specifies TWS ClientID Settings. Default is *1*.

Returns:
  - None

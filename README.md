# Mean Reversion Stock Trading System
*Made by rawsashimi1604*

### Introduction
Hey everyone! :wave: This is a stock trading system that I developed, using a trading software called **Amibroker, Python and TWS Interactive Brokers API**.

Huge thanks to *erdiwit* for creating ib_insync class to make programming this much more linear!

### How the trading system works?

#### Research material and background
For starters, I was looking into some stock trading strategies and methods that have proved profitable so far. I came across this book, **Short Term Trading Strategies that Work by Larry Connors.**

Larry described some useful pointers backed by statistics such as:
- Buying pullbacks, and using the Relative Strength Index (RSI) to detect them,
- Buy stocks in an uptrend,
- Using intra-day pullbacks to get a better entry price.

As such, I used some of his parameters and tested it out on a backtesting software, **Amibroker.**

#### Trading System
Here were the **parameters** I used for my trading system.

> *Moving Average Period* = 100
> *RSI Period* = 2
> *RSI Buy Signal* = 5
> *RSI Exit Signal* = 40
> *Max Positions to Hold* = 3
> *Exit After n Days* = 10
> *Limit Order* = 1.5%












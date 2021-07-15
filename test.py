# import talib
# from get_yf_data import *

# ticker = "MSFT"
# yf = Yahoo_Data(1, 5)

# # Get Data from Yahoo Finance
# ticker_close_data = yf.get_close(f'{ticker}')

# # Get Values for SMA, RSI Entry and ROC
# # sma_val = round(talib.SMA(ticker_close_data, 100).values.tolist()[-1], 2)
# # rsi_entry_val = round(talib.RSI(ticker_close_data, 2).values.tolist()[-1], 2)
# # roc_val = round(talib.ROC(ticker_close_data, 100).values.tolist()[-1], 2)


# print(ticker_close_data)

import yfinance as yf

apple = yf.Ticker("aapl")
dl = yf.download("AAPL", start="2021-07-12", period = "1d")

print(dl)
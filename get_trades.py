import pandas as pd
import numpy as np
import talib
from get_data import data, prevClose
from datetime import date

# Dataframe Settings
pd.set_option('display.max_columns', None)


def run_data_check():
    with open('S&P500 Components.csv', 'r') as f:
        df = pd.read_csv(f)
        df = df.set_index('Ticker')

        error_list = []

        for ticker in df.index:
            try:
                # Get Data from Yahoo Finance
                ticker_close_data = data(f'{ticker}')['Close']
                sma_test = round(talib.SMA(ticker_close_data, 100).values.tolist()[-1], 2)

            except:
                # Print out statement error if unable to pool data from Yahoo Finance
                print(f"Error in loading {ticker} data from Yahoo Finance. Will be removed from list.")
                error_list.append(f'{ticker}')

        print(error_list)
        return error_list


def get_trade_list(file_type):
    with open('S&P500 Components.csv', 'r') as f:
        # Lists to add in dataframe
        ytd_close = []
        sma = []
        roc = []
        rsi_entry = []
        buy_limit = []

        df = pd.read_csv(f)
        df = df.set_index('Ticker')

        # For loop to get TA Values
        for ticker in df.index:
            # Try to get Data from Yahoo Finance using Ticker
            try:
                # Get Data from Yahoo Finance
                ticker_close_data = data(f'{ticker}')['Close']

                # Get Values for SMA, RSI Entry and ROC
                sma_val = round(talib.SMA(ticker_close_data, 100).values.tolist()[-1], 2)
                rsi_entry_val = round(talib.RSI(ticker_close_data, 2).values.tolist()[-1], 2)
                roc_val = round(talib.ROC(ticker_close_data, 100).values.tolist()[-1], 2)

                # Get Yesterday's Close Value
                close_val = prevClose(f'{ticker}')

                # Add these values to existing lists
                sma.append(sma_val)
                roc.append(roc_val)
                rsi_entry.append(rsi_entry_val)
                ytd_close.append(close_val)
                buy_limit.append(round(close_val * 0.98, 2))

            except:
                # If not pass and continue line of code
                print(f"Error found in retrieving data from {ticker}.")
                # Drop row by index if not found.
                df = df.drop(f'{ticker}')
                pass

        # Add these values into pandas dataframe
        df['sma'] = sma
        df['roc'] = roc
        df['rsi_entry'] = rsi_entry
        df['ytd_close'] = ytd_close
        df['buy_limit'] = buy_limit

        # Remove tickers who do not meet criteria of Trading System
        df = df.drop(df[(df.rsi_entry > 5) | (df.ytd_close < 5) | (df.ytd_close < df.sma)].index)

        # Remove tickers who has NaN values
        df = df.dropna()

        # Sort rows by ROC Value
        df = df.sort_values(by=['roc'], ascending=False)

        # Print out new dataframe on a CSV file.
        # Get today's Date
        today = date.today()

        # Get top 5 trades
        df = df.iloc[:5]

        if file_type == "csv":
            # Export to CSV
            df.to_csv(f'{today} Reversion Trades.csv')

        elif file_type == "txt":
            # Export to Text
            df.to_csv(f'{today} Reversion Trades.txt', sep='\t')

        else:
            print("File Type invalid. Please key in either csv or txt.")

        # Print dataframe
        print(df)


def trade_list(file_csv):
    # Returns list of trades with Ticker and Buy Limit Price.
    # Requires get_trade_list("csv") in same directory to use.

    with open(f'{file_csv}', 'r') as f:
        df = pd.read_csv(f)
    df = df.set_index('Ticker')

    # Lists to append and print
    ticker = []
    buy_limit = []

    # For loop to append lists
    for stock in df.index:
        # Get Buy Price from dataframe
        buy_price = df.loc[f'{stock}'].get('buy_limit')
        # Add ticker and buy price into lists
        ticker.append(stock)
        buy_limit.append(buy_price)

    df = pd.DataFrame(buy_limit, index=ticker, columns=['buy_limit'])
    return df


def rsi_exit(ticker):
    # Get close data from Yahoo Finance
    ticker_close_data = data(f'{ticker}')['Close']

    # Get RSI Exit Val
    rsi_exit_val = round(talib.RSI(ticker_close_data, 5).values.tolist()[-1], 2)
    return rsi_exit_val


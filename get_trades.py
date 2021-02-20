import pandas as pd
import numpy as np
import talib
from get_yf_data import Yahoo_Data
from datetime import date

# Dataframe Settings
pd.set_option('display.max_columns', None)

# Initialize Yahoo_Data Class
yf = Yahoo_Data(1, 1, False)

def get_trade_list(file_type, components_path = "C:\\Users\\Gavin\\VisualStudio\\Reversion_Sys\\ReversionSys\\S&P500 Components.csv", export_path = "C:\\Users\\Gavin\\VisualStudio\\Reversion_Sys\\ReversionSys"):
    with open(components_path, 'r') as f:

        # If incorrect arguments, stop code.
        if file_type != 'csv' and 'txt':
            print("File type invalid. Please key in either 'csv' or 'txt'.")
            exit()

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
                ticker_close_data = yf.get_close(f'{ticker}')

                # Get Values for SMA, RSI Entry and ROC
                sma_val = round(talib.SMA(ticker_close_data, 100).values.tolist()[-1], 2)
                rsi_entry_val = round(talib.RSI(ticker_close_data, 2).values.tolist()[-1], 2)
                roc_val = round(talib.ROC(ticker_close_data, 100).values.tolist()[-1], 2)

                # Get Yesterday's Close Value
                close_val = yf.get_prevclose(f'{ticker}')

                # Add these values to existing lists
                sma.append(sma_val)
                roc.append(roc_val)
                rsi_entry.append(rsi_entry_val)
                ytd_close.append(close_val)
                buy_limit.append(round(close_val * 0.98, 2))

                # Output to run window.
                print(f"Download Success : {ticker}.")

            except Exception:
                # If not pass and continue line of code
                print(f"Error found in retrieving data from {ticker}.")
                # Try to change ticker "." to "-" to draw data from yahoo finance.
                ticker = ticker.replace(".", "-")
                print(f"New Ticker name updated {ticker}. Trying to update new TA data now.")
                try:
                    ticker_close_data = yf.get_close(f'{ticker}')

                    # Get Values for SMA, RSI Entry and ROC
                    sma_val = round(talib.SMA(ticker_close_data, 100).values.tolist()[-1], 2)
                    rsi_entry_val = round(talib.RSI(ticker_close_data, 2).values.tolist()[-1], 2)
                    roc_val = round(talib.ROC(ticker_close_data, 100).values.tolist()[-1], 2)

                    print(f"{ticker}: sma_val = {sma_val}")

                    # Get Yesterday's Close Value
                    close_val = yf.get_prevclose(f'{ticker}')

                    # Add these values to existing lists
                    sma.append(sma_val)
                    roc.append(roc_val)
                    rsi_entry.append(rsi_entry_val)
                    ytd_close.append(close_val)
                    buy_limit.append(round(close_val * 0.98, 2))

                    # Output to run window.
                    print(f"Download Success : {ticker}.")

                except Exception:
                    # If there is still an error, remove the ticker from the dataframe.
                    print(f"Still unable to get data from {ticker}. Removing from dataframe.")
                    df = df.drop(labels=f"{ticker}")

        # Add these values into pandas dataframe
        df['sma'] = sma
        df['roc'] = roc
        df['rsi_entry'] = rsi_entry
        df['ytd_close'] = ytd_close
        df['buy_limit'] = buy_limit

        # Remove tickers who do not meet criteria of Trading System
        df = df.drop(df[(df.rsi_entry > 5) | (df.roc < 0) | (df.ytd_close < 5) | (df.ytd_close < df.sma)].index )

        # Remove tickers who has NaN values
        df = df.dropna()

        # Sort rows by ROC Value
        df = df.sort_values(by=['roc'], ascending=False)

        # Get today's Date
        today = date.today()

        # Get top 3 trades
        df = df.iloc[:3]

        # Get directory path to export csv to
        path = f'{export_path}\\'

        if file_type == "csv":
            df.to_csv(path + f'{today} Reversion Trades.csv')

        elif file_type == "txt":
            df.to_csv(f'{today} Reversion Trades.txt', sep='\t')
            
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


# Exit criteria #1
def rsi_exit(ticker):
    # Get close data from Yahoo Finance
    ticker_close_data = yf.get_close(f'{ticker}')

    # Get RSI Exit Val
    rsi_exit_val = round(talib.RSI(ticker_close_data, 5).values.tolist()[-1], 2)
    return rsi_exit_val


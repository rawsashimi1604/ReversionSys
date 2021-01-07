from ibkr_account import *
from get_trades import *
import pandas as pd
import numpy as np
import math
from ib_insync import *

# Connect to IB Servers
ibkr.connect('127.0.0.1', 7497, clientId=1)

# Run Program when Market Opens

# Get Open Positions from IB
# Get number of positions left open in IB
positions = ibkr.positions()
positions_count = len(positions)

# Exit Positions if Criteria is met

# Import Trade_List aka Screener
screener_df = trade_list('2021-01-07 Reversion Trades.csv')
screener_list = list(screener_df.index.values)

# Get Account Dataframe
df = ib_account()

# Get account value in Base Currency
nlv_val = net_liquidation_value(df)

# Get account value in USD
nlv_val_usd = math.floor(nlv_val / usd_sgd_rate())
print(f"Net Liquidation Value in USD : ${nlv_val_usd}")

# Get amount to buy per position
per_stock = round(0.198 * nlv_val_usd, 2)
print(f"Amount allocated to each position : ${per_stock}")

# Check if any open positions corresponds to the trade_list, if it corresponds drop from trade_list
# Get Dataframe for open positions
positions_df = util.df(positions)

# Create list to store positions
positions_list = []

# Loop through 0,1,2,3,4 index to get current open positions
for x in range(0, 5):
    # Try to find the positions in positions_df
    try:
        # Try to find positions_ticker using tradingClass
        try:
            positions_ticker = positions_df.iloc[x, 1].tradingClass
            # Store them in the new list
            positions_list.append(f'{positions_ticker}')

        # No trades found using tradingClass, hence no trades, hence pass line of code
        except AttributeError:
            pass

    # If unable to find, pass and continue code
    except IndexError:
        pass

# Loop through 1,2,3,4 index to get current positions.
for x in range(0, 5):
    try:
        # Get Ticker from current positions using list index.
        ticker = positions_list[x]
        if ticker in screener_list:
            # Remove if position corresponds to screener.
            print(f"{ticker} is currently open. Will not enter {ticker} position today.")
            screener_df = screener_df.drop(f'{ticker}')
            screener_list.remove(f'{ticker}')

    # If unable to find any corresponding positions, pass and continue code
    except IndexError:
        pass

# Count number of positions to enter today.
positions_to_enter = 5 - positions_count

# Create a list to store positions entered.
current_positions = []

# Add 2 blank spaces for a neater run window.
print("")
print("")

# Send Orders from CSV File using For Loop, whilst entering number of positions to enter today.
for ticker in screener_df.index[:positions_to_enter]:
    # Create a object to send to IB
    stock_ticker = f'{ticker}'

    # Stock Object
    contract = Stock(f'{stock_ticker}', 'SMART', 'USD')

    # Get Price to Limit Buy
    price = screener_df.loc[f'{ticker}', 'buy_limit']

    # Get Quantity to Limit Buy
    qty = math.floor(per_stock / price)

    # Order Object
    order = LimitOrder("BUY", f'{qty}', f'{price}')

    # Send Order using Ticker Object and Order Object, Returns Trade Class
    trade = ibkr.placeOrder(contract, order)

    # Print Orders sent and append list.
    print(f"BuyLimit {ticker} @ {price}. Quantity = {qty}. Order has been sent.")
    current_positions.append(f'{ticker}')

    # Sleep buffer of 0.5 seconds
    ibkr.sleep(0.5)

# Output to run window.
print(f'''
Current Open Positions: {positions_list}
Positions entered: {current_positions}. Total Positions entered: {positions_to_enter}.
''')

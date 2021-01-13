from ibkr_account import *
from get_trades import *
import pandas as pd
import numpy as np
import math
from ib_insync import *
from datetime import datetime
from sys import exit


def sell_positions():
    # Copyright
    # Get current date time.
    now = datetime.now()

    # Output to run
    print(f'''
    ****************************** ReversionSys System made by Gavin Loo Dec 2020 ******************************
    Programmed in Python 3.9.
    Current Date and Time is {now.strftime("%d/%m/%Y %H:%M:%S")}
    ---------------------------------------------------------------------------------------------------------------------

    *IMPORTANT*
    Please only run after entering 10 days n Bars trailing stop loss as this version does not support that exit feature.
    ---------------------------------------------------------------------------------------------------------------------
    ''')
    # Connect to IB Servers
    try:
        ibkr.connect('127.0.0.1', 7497, clientId=1)
        print("Connecting to Interactive Brokers TWS Servers.")

    except ConnectionRefusedError:
        # If connection does not work, end the program.
        print('''Error in connecting to Interactive Brokers TWS Servers.
    Please check your Internet connection, IP Address, Socket port number.
    Check TWS Settings to see if API "READ - ONLY API" is disabled, and ports are allowed to connect.
    .......
    Ending program now.
            ''')
        exit(0)

    # Connection is successful continuing next line of code.
    print('''Connection successful. Will continue placing trades now.
    ---------------------------------------------------------------------------------------------------------------------
    ''')

    # Get Open Positions from IB
    # Get number of positions left open in IB
    positions = ibkr.positions()
    positions_count = len(positions)

    # Get Dataframe for open positions
    positions_df = util.df(positions)

    # Create list to store positions
    positions_list = []

    # Loop through 0,1,2,3,4 index to get current open positions.
    for x in range(0, 5):
        # Try to find the positions in positions_df
        try:
            # Try to find positions_ticker using tradingClass
            try:
                positions_ticker = positions_df.iloc[x, 1].symbol
                # Store them in the new list
                positions_list.append(f'{positions_ticker}')

            # No trades found using tradingClass, hence no trades, hence pass line of code
            except AttributeError:
                pass
        # If unable to find, pass and continue code
        except IndexError:
            pass

    # Output to run window
    print(f"Total positions : {positions_count}, Active Positions: {positions_list}")

    # Run if there are open positions, check for exits.
    if positions_count > 0:
        # Output to run window
        print('''There are open positions, will check for any exit signals now.
    ---------------------------------------------------------------------------------------------------------------------
    ''')

        # Create list to store position qty
        qty_list = []

        # Get Quantity per position
        for x in range(0, 5):
            # Try to get position qty
            try:
                # Get Position qty
                pos_size = positions_df.iloc[x, 2]
                qty_list.append(pos_size)

            # If not continue on with next line of code.
            except IndexError:
                pass

        # Create a list to store exit positions.
        exit_positions = []

        # Check RSI Value of each position
        for ticker in positions_list:
            # Get RSI Value
            rsi_val = rsi_exit(f'{ticker}')
            if rsi_val > 40:
                exit_positions.append(f'{ticker}')
            else:
                pass

        # Count number of exit positions
        exit_positions_count = len(exit_positions)

        count = 0
        # Exit Orders if Exit condition is met.
        for ticker in exit_positions:
            try:
                # Stock Object
                contract = Stock(f'{ticker}', 'SMART', 'USD')

                # Order Object
                order = MarketOrder("SELL", f"{qty_list[count]}")

                # Send Order using Ticker Object and Order Object, Returns Trade Class
                trade = ibkr.placeOrder(contract, order)

                # Print Orders sent and append list.
                print(f'''
    MarketSell {ticker}. Quantity = {qty_list[count]}. Order has been sent.''')

                # Sleep buffer of 0.5 seconds
                ibkr.sleep(0.5)

                # Output to run window.
                print(f'''
                Positions exited: {exit_positions}. Total Positions entered: {exit_positions_count}
    ---------------------------------------------------------------------------------------------------------------------
                ''')

                # Count ++ to continue loop until 4
                count += 1

            except IndexError:
                print("No more elements in qty_list. Will continue next line of code now.")
                pass


def buy_positions():
    # Copyright
    # Get current date time.
    now = datetime.now()

    # Output to run
    print(f'''
        ****************************** ReversionSys System made by Gavin Loo Dec 2020 ******************************
        Programmed in Python 3.9.
        Current Date and Time is {now.strftime("%d/%m/%Y %H:%M:%S")}
        ---------------------------------------------------------------------------------------------------------------------

        *IMPORTANT*
        Please only run after entering 10 days n Bars trailing stop loss as this version does not support that exit feature.
        ---------------------------------------------------------------------------------------------------------------------
        ''')
    # Connect to IB Servers
    try:
        ibkr.connect('127.0.0.1', 7497, clientId=1)
        print("Connecting to Interactive Brokers TWS Servers.")

    except ConnectionRefusedError:
        # If connection does not work, end the program.
        print('''Error in connecting to Interactive Brokers TWS Servers.
        Please check your Internet connection, IP Address, Socket port number.
        Check TWS Settings to see if API "READ - ONLY API" is disabled, and ports are allowed to connect.
        .......
        Ending program now.
                ''')
        exit(0)

    # Connection is successful continuing next line of code.
    print('''Connection successful. Will continue placing trades now.
        ---------------------------------------------------------------------------------------------------------------------
        ''')
    # Import Trade_List aka Screener
    screener_df = trade_list('2021-01-12 Reversion Trades.csv')
    screener_list = list(screener_df.index.values)

    # Get Open Positions from IB
    # Get number of positions left open in IB
    positions = ibkr.positions()
    positions_count = len(positions)

    # Get Dataframe for open positions
    positions_df = util.df(positions)

    # Create list to store positions
    positions_list = []

    # Loop through 0,1,2,3,4 index to get current open positions.
    for x in range(0, 5):
        # Try to find the positions in positions_df
        try:
            # Try to find positions_ticker using tradingClass
            try:
                positions_ticker = positions_df.iloc[x, 1].symbol
                # Store them in the new list
                positions_list.append(f'{positions_ticker}')

            # No trades found using tradingClass, hence no trades, hence pass line of code
            except AttributeError:
                pass
        # If unable to find, pass and continue code
        except IndexError:
            pass

    # Get Account Dataframe
    df = ib_account()

    # Get account value in Base Currency
    nlv_val = net_liquidation_value(df)

    # Get account value in USD
    nlv_val_usd = math.floor(nlv_val / usd_sgd_rate())
    print(f'''
    Net Liquidation Value in USD : ${nlv_val_usd}''')

    # Get amount to buy per position
    per_stock = round(0.32 * nlv_val_usd, 2)
    print(f'''Amount allocated to each position : ${per_stock}
    ---------------------------------------------------------------------------------------------------------------------
    ''')

    # Check if any open positions corresponds to the trade_list, if it corresponds drop from trade_list
    # Loop through 0,1,2,3,4 index to remove corresponding positions.
    for x in range(0, 5):
        # Try to find any corresponding positions, remove ticker from dataframe if found.
        try:
            # Get Ticker from current positions using list index.
            ticker = positions_list[x]
            if ticker in screener_list:
                # Remove if position corresponds to screener.
                print(f'''
    {ticker} is currently open. Will not enter {ticker} position today.
    ---------------------------------------------------------------------------------------------------------------------
    ''')
                screener_df = screener_df.drop(f'{ticker}')
                screener_list.remove(f'{ticker}')

        # If unable to find any corresponding positions, pass and continue code
        except IndexError:
            pass

    # Output to run
    print(f'''
    Positions to enter today: {screener_list}
    ---------------------------------------------------------------------------------------------------------------------
    ''')

    # Count number of positions to enter today.
    positions_to_enter = 3 - positions_count

    # Create a list to store positions entered.
    current_positions = []

    # Send Orders from CSV File using For Loop, whilst entering number of positions to enter today.
    for ticker in screener_df.index[:positions_to_enter]:
        # Create a object to send to IB
        stock_ticker = f'{ticker}'

        # Stock Object
        contract = Stock(f'{stock_ticker}', 'ISLAND', 'USD')

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
    Positions left to enter: {positions_to_enter}.
    Positions entered: {current_positions}.
    Total Positions entered: {len(current_positions)}.
    End of program...
    ---------------------------------------------------------------------------------------------------------------------
    ''')


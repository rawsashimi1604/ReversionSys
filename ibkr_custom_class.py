from get_yf_data import Yahoo_Data
from get_trades import *
from misc_func import list_to_str
import pandas as pd
import numpy as np
import math
from ib_insync import *
from datetime import datetime
from sys import exit

class Interactive_Brokers_Custom:
    ### Commands for interative brokers bot ###
    # Initialize IB class as ibkr
    ibkr = IB()

    # Get current date time.
    now = datetime.now()

    def __init__(self, name, max_pos):
        # Initializes Interactive_Brokers_Custom Class
        self.name = name
        self.max_pos = max_pos

    def intro(self):
        # Output to run
        print(f'''
********************************** ReversionSys System made by Gavin Loo Dec 2020 ***********************************
Programmed in Python 3.7.
Current Date and Time is {Interactive_Brokers_Custom.now.strftime("%d/%m/%Y %H:%M:%S")}
---------------------------------------------------------------------------------------------------------------------

*IMPORTANT*
Please only run after entering 10 days n Bars trailing stop loss as this version does not support that exit feature.
---------------------------------------------------------------------------------------------------------------------
        ''')


    def connect(self):
        # Connects to ibkr TWS server to run bot.
        # Connect to IB Servers
        try:
            Interactive_Brokers_Custom.ibkr.connect('127.0.0.1', 7497, clientId=1)
            print("Connecting to Interactive Brokers TWS Servers......")

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
        print('''
Connection to Interactive Brokers server successful.
---------------------------------------------------------------------------------------------------------------------
        ''')
        

    def get_account(self):
        # Returns Dataframe of Account Information
        # Find Account Name
        account = Interactive_Brokers_Custom.ibkr.managedAccounts()[0]
        acc_str = list_to_str(account)

        # Get Account Summary Dataframe
        acc_val_list = Interactive_Brokers_Custom.ibkr.accountSummary(acc_str)
        df = util.df(acc_val_list)
        df = df.set_index('tag')

        # Return Dataframe as output
        return df


    def usd_sgd_rate(self):
        # Gets the current USD_SGD Exchange Rate

        pair_name = Forex('USDSGD')
        bars = Interactive_Brokers_Custom.ibkr.reqHistoricalData(
            pair_name, endDateTime='', durationStr='300 S',
            barSizeSetting='5 mins', whatToShow='MIDPOINT', useRTH=True)
        df = util.df(bars)
        df = df.tail(1)
        val = df['close'].values[0]
        return val


    def net_liquidation_value(self, dataframe):
        df = dataframe
        nlv_val = float(df.loc['NetLiquidation'].get('value'))
        return nlv_val


    def buying_power(self, dataframe):
        df = dataframe
        bp_val = float(df.loc['BuyingPower'].get('value'))
        return bp_val


    def sell_positions(self):
        # Get Open Positions from IB
        # Get number of positions left open in IB
        positions = Interactive_Brokers_Custom.ibkr.positions()
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
            print('''
There are open positions, will check for any exit signals now.
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

            if exit_positions_count == 0:
                print("No postiions to be exited.")
            
            count = 0
            # Exit Orders if Exit condition is met.
            for ticker in exit_positions:
                try:
                    # Stock Object
                    contract = Stock(f'{ticker}', 'SMART', 'USD')

                    # Order Object
                    order = MarketOrder("SELL", f"{qty_list[count]}")

                    # Send Order using Ticker Object and Order Object, Returns Trade Class
                    trade = Interactive_Brokers_Custom.ibkr.placeOrder(contract, order)

                    # Print Orders sent and append list.
                    print(f'''
MarketSell {ticker}. Quantity = {qty_list[count]}. Order has been sent.
''')

                    # Sleep buffer of 0.5 seconds
                    Interactive_Brokers_Custom.ibkr.sleep(0.5)

                    # Count ++ to continue loop until 4
                    count += 1

                except IndexError:
                    print("No more elements in qty_list. Will continue next line of code now.")
                    pass
        
        # Output to run window on summary
                print(f'''
Positions exited: {exit_positions}. Total Positions exit: {exit_positions_count}
End of sell function
---------------------------------------------------------------------------------------------------------------------
                ''')

    def buy_positions(self, buy_list):
        # Output to run.
        print(f'''
Max Positions Available : {self.max_pos}
Will execute buy program based on max positions available.
---------------------------------------------------------------------------------------------------------------------
        ''')
        # Import Trade_List aka Screener
        screener_df = trade_list(f'{buy_list}')
        screener_list = list(screener_df.index.values)

        # Get Open Positions from IB
        # Get number of positions left open in IB
        positions = Interactive_Brokers_Custom.ibkr.positions()
        positions_count = len(positions)

        # Get Dataframe for open positions
        positions_df = util.df(positions)

        # Create list to store positions
        positions_list = []

        # Loop through 0,1,2,3,4 index to get current open positions.
        for x in range(0, self.max_pos):
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
        df = self.get_account()

        # Get default currency
        currency = df.loc['NetLiquidation', 'currency']

        # Get account value in Base Currency
        nlv_val = self.net_liquidation_value(df)

        if currency == 'SGD':
            # Get account value in USD
            nlv_val_usd = math.floor(nlv_val / self.usd_sgd_rate())
            print(f'''
Account base currency is in SGD. Net Liquidation Value in USD shall be calculated.
Net Liquidation Value in USD : ${nlv_val_usd}
            ''')

        elif currency == 'USD':
            # Else NLV shall be in USD.
            nlv_val_usd = nlv_val
            print(f'''
Account base currency is in USD. No conversion needed.
Net Liquidation Value in USD : ${nlv_val_usd}
            ''')

        else:
            # If account is not in SGD or USD, program cannot be run. Shall exit code now.
            print('Account base currency is neither USD or SGD. Ending program now.')
            exit(0)

        # % per position according to number of positions, given a buffer of 0.5%
        prc_position = ((100 / self.max_pos) * 0.995) / 100

        # Get amount to buy per position
        per_stock = round(prc_position * nlv_val_usd, 2)
        print(f'''
Amount allocated to each position : ${per_stock}
---------------------------------------------------------------------------------------------------------------------
        ''')

        # Check if any open positions corresponds to the trade_list, if it corresponds drop from trade_list
        # Loop through 0,1,2,3,4 index to remove corresponding positions.
        for x in range(0, self.max_pos):
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
        positions_to_enter = self.max_pos - positions_count

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
            trade = Interactive_Brokers_Custom.ibkr.placeOrder(contract, order)

            # Print Orders sent and append list.
            print(f"BuyLimit {ticker} @ {price}. Quantity = {qty}. Order has been sent.")
            current_positions.append(f'{ticker}')

            # Sleep buffer of 0.5 seconds
            Interactive_Brokers_Custom.ibkr.sleep(0.5)

        # Output to run window.
        print(f'''
Positions left to enter: {positions_to_enter}.
Positions entered: {current_positions}.
Total Positions entered: {len(current_positions)}.
End of program...
---------------------------------------------------------------------------------------------------------------------
        ''')


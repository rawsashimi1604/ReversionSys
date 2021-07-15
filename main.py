# Import custom classes from various .py files
from ibkr_custom_class import Interactive_Brokers_Custom
from get_yf_data import Yahoo_Data
from get_trades import get_trade_list
import pandas as pd
import datetime
import time

# Dataframe Settings
pd.set_option('display.max_columns', None)

def run_bot(path = "C:\\Users\\rawsashimi1604\\VisualStudio\\Reversion_Sys\\ReversionSys\\2021-01-25 Reversion Trades.csv", market_open_time = "22:30:05", ip='127.0.0.1', socket=7497, clientId=1):

    # Get Market Open timing in SGT with 5 seconds of buffer
    market_open =  market_open_time

    # Initialize custom class as ib for easier usage.
    ib = Interactive_Brokers_Custom('ReversionSys', 3)

    # Get intro message to output
    ib.intro()

    # Connect to interactive brokers TWS Server
    ib.connect(ip=ip, socket=socket, clientId=clientId)

    # Run bot loop
    while True:
        # Get current date and time in formatted string
        dt = datetime.datetime.now().strftime('%H:%M:%S')
        date = datetime.datetime.today().strftime('%Y-%m-%d')

        # Print time constantly and sleep 1 second for buffer
        print(f"Time now is : {dt}, Waiting for market open.")
        time.sleep(1)

        # If time == market open, run bot.
        if dt == market_open:
            print("Market has opened... will begin trading sequence now....")

            # Sell any positions that have exit criteria met.
            ib.sell_positions()

            # Sleep 2.5 seconds for buffer
            ib.ibkr.sleep(2.5)

            # Buy any positions that have entry criteria met.
            ib.buy_positions(f'{path}')

            time.sleep(1)
            exit(0)
            print(f"Finished executing code @ {dt}. Shutting down program now.")



# Run bot
# run_bot(path = r'C:\\Users\\Gavin\\VisualStudio\\Reversion_Sys\\ReversionSys\\2021-02-08 Reversion Trades.csv')

# Get Trade List
get_trade_list()

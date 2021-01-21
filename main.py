# Import custom classes from various .py files
from ibkr_custom_class import Interactive_Brokers_Custom
from get_yf_data import Yahoo_Data
from get_trades import get_trade_list
import datetime
import time


def run_bot():

    # Get Market Open timing in SGT
    market_open = "20:10:03"   

    # Initialize custom class as ib for easier usage.
    ib = Interactive_Brokers_Custom('ReversionSys', 3)

    # Get intro message to output
    ib.intro()

    # Connect to interactive brokers TWS Server
    ib.connect()

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
            # Output to run window
            print("Market has opened... will begin trading sequence now....")

            # Sell any positions that have exit criteria met.
            ib.sell_positions()

            # Sleep 2.5 seconds for buffer
            ib.ibkr.sleep(2.5)

            # Buy any positions that have entry criteria met.
            ib.buy_positions(f'C:\\Users\\Gavin\\VisualStudio\\Reversion_Sys\\ReversionSys\\{date} Reversion Trades.csv')

            # Sleep
            time.sleep(1)
    

# Run bot
# run_bot()

# Get Trade List
get_trade_list('csv')

# Import custom classes from various .py files
from ibkr_custom_class import Interactive_Brokers_Custom
from get_yf_data import Yahoo_Data

# Initialize custom class as ib for easier usage.
ib = Interactive_Brokers_Custom('ReversionSys', 3)

# Connect to interactive brokers TWS Server
ib.connect()

# Sell any positions that have exit criteria met.
ib.sell_positions()

# Sleep for buffer
ib.ibkr.sleep(5)

# Buy any positions that have entry criteria met.
ib.buy_positions('C:\\Users\\Gavin\\VisualStudio\\Reversion_Sys\\ReversionSys\\2021-01-18 Reversion Trades.csv')





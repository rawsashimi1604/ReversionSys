from ib_insync import *
from misc_func import list_to_str
import pandas as pd
import numpy as np
import math

# Wrapper to receive data from API
# Client to send data to API

# Initialize IB Class and connect to ibkr Servers
ibkr = IB()


def ib_account():
    # Returns Dataframe of Account Information
    # Find Account Name
    account = ibkr.managedAccounts()[0]
    acc_str = list_to_str(account)

    # Get Account Summary Dataframe
    acc_val_list = ibkr.accountSummary(acc_str)
    df = util.df(acc_val_list)
    df = df.set_index('tag')

    # Return Dataframe as output
    return df


def usd_sgd_rate():
    # Gets the current USD_SGD Exchange Rate
    # Requires ib_account() connection to use.

    pair_name = Forex('USDSGD')
    bars = ibkr.reqHistoricalData(
        pair_name, endDateTime='', durationStr='300 S',
        barSizeSetting='5 mins', whatToShow='MIDPOINT', useRTH=True)
    df = util.df(bars)
    df = df.tail(1)
    val = df['close'].values[0]
    return val


def net_liquidation_value(dataframe):
    # Requires ib_account() dataframe to use.
    df = dataframe
    nlv_val = float(df.loc['NetLiquidation'].get('value'))
    return nlv_val


def buying_power(dataframe):
    # Requires ib_account() dataframe to use.
    df = dataframe
    bp_val = float(df.loc['BuyingPower'].get('value'))
    return bp_val

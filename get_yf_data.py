import yfinance as yf
import pandas as pd
import pprint


# Yahoo Finance Data Class Create
class Yahoo_Data:
    # Initiate Class Self inputs
    def __init__(self, period_years, candle_interval, print=False):
        self.period_years = period_years
        self.candle_interval = candle_interval
        self.print = print

    # Info section of each stock
    def get_info(self, ticker, command="nil"):
        # Get Information of stock in dictionary format
        #### Important commands to get crucial information of stock: ####
            # averageVolume : Get Average Volume of Stock
            # currency : Get Currency of Stock
            # dividendYield : Get Dividend Yield of Stock
            # forwardEps : Get Forward Earnings per Share of Stock
            # forwardPE : Get Forward P/E Ratio of Stock
            # industry : Get Industry of Stock
            # longBusinessSummary : Get Business Summary of Stock
            # longName : Get Name of Stock
            # marketCap : Get Market Capitalization of Stock
            # pegRatio : Get Price to Earnings Growth Ratio of Stock
            # previousClose : Get Previous Close of Stock
            # priceToBook : Get Price to Book Ratio of Stock
            # quoteType : Get Type of Asset 

        ticker = yf.Ticker(ticker)
        if command == "nil":
            # if no command, prints out whole dictionary in a pprint format
            info = ticker.info
            if self.print == True:
                pprint.pprint(info)
        
        else:
            # else, print out value of key of dictionary
            info = ticker.info.get(f"{command}", "No such key exists. Please try again with a valid key.")
            if self.print == True:
                print(f"{command} : {info}")
        
        return info
  

    def get_data(self, ticker):
        # Download some market data.
        ticker = yf.Ticker(ticker)
        hist = ticker.history(period=f"{self.period_years}y",interval=f"{self.candle_interval}d")
        if self.print == True:
            pprint.pprint(hist)
        return hist


    def get_ohlc(self, ticker):
        # Get OHLC for stock
        ticker = yf.Ticker(f"{ticker}")
        ohlc = ticker.history(period=f"{self.period_years}y",interval=f"{self.candle_interval}d")
        if self.print == True:
            pprint.pprint(ohlc)
        return ohlc


    def get_close(self, ticker):
        # Get close data for stock
        ticker = yf.Ticker(f"{ticker}")
        close = ticker.history(period=f"{self.period_years}y",interval=f"{self.candle_interval}d")['Close']
        if self.print == True:
            pprint.pprint(close)
        return close


    def get_prevclose(self, ticker):
        # Get Previous close value for stock
        ticker = yf.Ticker(f"{ticker}")
        prev_close = ticker.history(period=f"{self.period_years}y",interval=f"{self.candle_interval}d")['Close']
        val = round(prev_close.iloc[-1],2)
        if self.print == True:
            pprint.pprint(val)
        return val


    def get_bal_sheet(self, ticker, period="yearly"):
        # Get balance sheet data for stock
        ticker = yf.Ticker(f"{ticker}")

        # Get yearly balance sheet
        if period == "yearly":
            bal_sheet = ticker.balance_sheet
            if self.print == True:
                pprint.pprint(bal_sheet)
        
        # Get quarterly balance sheet
        elif period == "quarterly":
            bal_sheet = ticker.quarterly_balance_sheet
            if self.print == True:
                pprint.pprint(bal_sheet)
        
        # Error if input wrong kwargs
        else:
            print("Invalid statement. Please use either 'yearly' or 'quarterly' for period input.")
            bal_sheet = 'Error'
        
        return bal_sheet

    def get_recc(self, ticker):
        # Get analysts recommendations for stock
        ticker = yf.Ticker(f"{ticker}")
        recc = ticker.recommendations
        if self.print == True:
            pprint.pprint(recc)
        return recc    


    def get_calendar(self, ticker):
        # Get next event, earnings etc.
        ticker = yf.Ticker(f"{ticker}")
        calendar = ticker.calendar
        if self.print == True:
            pprint.pprint(calendar)
        return calendar




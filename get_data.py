import yfinance as yf


def data(tickerName):
    # Download some market data.
    ticker = yf.Ticker(tickerName)
    hist = ticker.history(period="1y",interval="1d")
    return hist


def prevClose(tickerName):
    ticker = yf.Ticker(f"{tickerName}")
    prev_close = ticker.history(period="1d",interval="1d")['Close']
    val = round(prev_close.iloc[0],2)
    return val


def list_to_str(list1):
    list_str = "".join(list1)
    return list_str

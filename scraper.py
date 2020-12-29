# Import dependencies
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime, timedelta

def Scrape(ticker):
    """
    Scrape stock data for specified ticker and return dictionary
    """
    today = datetime.today()
    yesterday = today - timedelta(days=1)
    df = web.DataReader(ticker, 'yahoo', yesterday, today)  # Scrape todays stock data for specified ticker
    # Format each stock attribute
    date = df.index.tolist()[0].strftime("%d-%m-%Y")
    high = round(df['High'].tolist()[0], 2)
    low = round(df['Low'].tolist()[0], 2)
    open = round(df['Open'].tolist()[0], 2)
    close = round(df['Close'].tolist()[0], 2)
    volume = df['Volume'].tolist()[0]
    adj_close = round(df['Adj Close'].tolist()[0], 2)
    # Construct dictionary
    data = {'date':date,'high':high,'low':low,'open':open,'close':close,'volume':volume,'adj_close':adj_close}
    return data
import yfinance as yf


def get_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    return data

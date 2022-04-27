import pandas as pd


class MACD:
    def __init__(self, fast, slow, smooth, price):
        self.price = pd.DataFrame(price)
        self.fast = fast
        self.slow = slow
        self.smooth = smooth

    def get_macd(self):
        price = self.price['Price']
        exp1 = price.ewm(span=self.fast, adjust=False).mean()
        exp2 = price.ewm(span=self.slow, adjust=False).mean()
        macd = pd.DataFrame(exp1 - exp2).rename(columns={'Price': 'MACD'})
        signal = pd.DataFrame(macd.ewm(span=self.smooth, adjust=False).mean()).rename(columns={'MACD': 'Signal'})

        return pd.concat([macd, signal, self.price], join='inner', axis=1)

    def calculate_signals(self):
        hist = self.get_macd()
        return hist.apply(self.manage_position, raw=False, axis=1)

    def manage_position(self, x):
        if x[0] > x[1]:
            return True
        return False

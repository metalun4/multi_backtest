import pandas as pd
import numpy as np


class WTLB:
    def __init__(self, clength, alength, price):
        self.price = price
        self.clength = clength
        self.alength = alength
        self.signal = False

    def get_wtlb(self):
        price = self.price['Price']
        esa = price.ewm(span=self.clength, adjust=False).mean()
        pmes = price - esa
        d = np.absolute(pmes).ewm(span=self.clength, adjust=False).mean()
        ci = pmes / (0.015 * d)
        tci = ci.ewm(span=self.alength, adjust=False).mean()

        wt1 = pd.DataFrame(tci).rename(columns={0: 'WT1'})
        wt2 = pd.DataFrame(tci.rolling(4).mean()).rename(columns={0: 'WT2'})

        return pd.concat([wt1, wt2, self.price], join='inner', axis=1)

    def calculate_signals(self):
        hist = self.get_wtlb()
        return hist.apply(self.manage_position, raw=False, axis=1)

    def manage_position(self, x):
        if x[0] < -60:
            self.signal = True
        elif 60 < x[0]:
            self.signal = False

        return self.signal

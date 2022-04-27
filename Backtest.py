import pandas as pd
import matplotlib.pyplot as plt

from Utils import get_data
from Portfolio import Portfolio
from TA.MACD import MACD
from TA.WTLB import WTLB

plt.rcParams['figure.figsize'] = (20, 10)
plt.style.use('fivethirtyeight')


class Backtest:
    def __init__(self, options, portfolio=Portfolio()):
        self.options = options,
        self.portfolio = portfolio
        self.data = get_data(options['ticker'], options['period'], options['interval'])
        self.risk = options['risk']

    def get_signals(self):
        options = self.options
        signals = []
        avg_price = self.get_price()

        for ta in options[0]['ta']:
            if ta['name'] == 'MACD':
                macd_signal = MACD(ta['fast'], ta['slow'], ta['smooth'], avg_price).calculate_signals()
                signals.append(macd_signal)
            elif ta['name'] == 'WTLB':
                wtlb_signal = WTLB(ta['clength'], ta['alength'], avg_price).calculate_signals()
                signals.append(wtlb_signal)
            else:
                print('Invalid Technicals')
                return

        return pd.concat(signals, join='inner', axis=1)

    def get_price(self):
        return pd.DataFrame((self.data['High'] + self.data['Low'] + self.data['Close']) / 3).rename(columns={0: 'Price'})

    def calculate_portfolio(self):
        calculated_data = pd.concat([self.data['Close'], self.get_signals()], join='inner', axis=1)
        return calculated_data.apply(self.manage_positions, raw=False, axis=1)

    def manage_positions(self, x):
        portfolio = self.portfolio
        if x[0] is True and x[1] is True:
            cash_spent = float(portfolio.current_balance * self.risk)
            asset_amount = float(cash_spent / x['Close'])
            portfolio.open_position(cash_spent, asset_amount)
        elif x[1] is False:
            cash_back = float(portfolio.asset * x['Close'])
            portfolio.close_position(cash_back)

        return float(portfolio.current_balance + (portfolio.asset*x['Close']))

    def plot_strat(self):
        prices = self.data['Close']

        ax1 = plt.subplot2grid((11, 1), (0, 0), rowspan=5, colspan=1)
        ax2 = plt.subplot2grid((11, 1), (6, 0), rowspan=5, colspan=1)

        ax1.plot(prices, linewidth=1.5, label=['Price'])

        ax2.plot(self.calculate_portfolio(), color='black', linewidth=1.5, label='Cash')

        plt.legend(loc='lower right')

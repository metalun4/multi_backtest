import pandas as pd

class Portfolio:
    def __init__(self, initial_balance=10000):
        self.current_balance = initial_balance
        self.asset = 0

    def open_position(self, cash_deducted, asset_added):
        self.asset += asset_added
        self.current_balance -= cash_deducted

    def close_position(self, cash_added):
        self.asset = 0
        self.current_balance += cash_added

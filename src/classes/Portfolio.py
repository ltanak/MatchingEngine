from src.classes.User import User

"""
Class to store all corresponding user stock accounts
Returns specific account on query
"""

class Portfolio:

    def __init__(self, stocks: dict[str, User]):
        self.accounts = stocks

    def getAccount(self, accountCode):
        return self.accounts[accountCode]

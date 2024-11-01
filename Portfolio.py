from collections import deque
import random
import numpy as np
import heapq
import time
import math
import uuid
from Transaction import Transaction
from User import User

class Portfolio:

    def __init__(self, stocks: list[User]):
        self.accounts = {
            "MSFT": stocks[0],
            "AAPL": stocks[1], 
            "AMZN": stocks[2], 
            "GOOG": stocks[3],
            "INTC": stocks[4]
        }

    def getAccount(self, accountCode):
        return self.accounts[accountCode]

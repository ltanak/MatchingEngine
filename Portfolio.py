from collections import deque
import random
import numpy as np
import heapq
import time
import math
import uuid
from Transaction import Transaction
from User import User

"""
Class to store all corresponding user stock accounts
Returns specific account on query
"""

class Portfolio:

    def __init__(self, stocks: dict[str, User]):
        self.accounts = stocks

    def getAccount(self, accountCode):
        return self.accounts[accountCode]

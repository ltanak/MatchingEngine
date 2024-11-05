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

    def __init__(self, stocks: dict[str, User]):
        self.accounts = stocks

    def getAccount(self, accountCode):
        return self.accounts[accountCode]

import random
import numpy as np
import heapq
import time
import math
import uuid

class Transaction:

    def __init__(self, generate = False, timestamp = None, id = None, type = "BID", price = None, quantity = None):
        self.timestamp = timestamp
        self.id = id
        self.type = type # "BID / BUY" vs "ASK / SELL"
        self.price = price
        self.quantity = quantity
        if generate:
            self.generateOrder()

    def generateOrder(self):
        self.timestamp = time.time()
        self.id = uuid.uuid4()
        self.price = random.randint(1, 100)
        self.quantity = random.randint(1, 10000)

import random
import numpy as np
import heapq
import time
import math

class Transaction:

    def __init__(self, timestamp, id, type, price, quantity):
        self.timestamp = timestamp
        self.id = id
        self.type = type # "BID / BUY" vs "ASK / SELL"
        self.price = price
        self.quantity = quantity

    def generateOrder(self):
        self.timestamp = time.time()

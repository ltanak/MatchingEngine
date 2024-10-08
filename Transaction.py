import random
import numpy as np
import heapq
import time
import math
import uuid

class Transaction:

    def __init__(self, fromCSV = [], generate = False):
        self.timestamp = -1
        self.id = -1
        self.type = None
        self.price = -1
        self.quantity = -1
        if len(fromCSV) != 0:
            self.createTransactionCSV(fromCSV)
        if generate:
            self.generateOrder()

    def generateOrder(self):
        self.timestamp = time.time()
        self.id = uuid.uuid4()
        self.price = random.randint(1, 100)
        self.quantity = random.randint(1, 10)
        if random.randint(1,2) == 1:
            self.type == "BID"
        else:
            self.type == "ASK"

    def createTransactionCSV(self, csvInputArray):
        self.timestamp = float(csvInputArray[0])
        self.id = int(csvInputArray[2])
        self.quantity = float(csvInputArray[3])
        self.price = float(csvInputArray[4])
        if csvInputArray[5] == "1":
            self.type = "BID"
        else:
            self.type = "ASK"

    def setTransaction(self, timestamp, id, type, price, quantity):
        self.timestamp = timestamp
        self.id = id
        self.type = type
        self.price = price
        self.quantity = quantity

    def reduceQuantity(self, value):
        self.quantity -= value

    def __eq__(self, otherTransaction: object) -> bool:
        if not isinstance(otherTransaction, Transaction):
            raise TypeError("Cannot compare these two object types")
        if self.id == otherTransaction.id:
            return True
        return False
    
    def __gt__(self, otherTransaction):
        if not isinstance(otherTransaction, Transaction):
            raise TypeError("Cannot compare these two object types")
        if self.id > otherTransaction.id:
            return True
        return False
    
    def __lt__(self, otherTransaction):
        if not isinstance(otherTransaction, Transaction):
            raise TypeError("Cannot compare these two object types")
        if self.id < otherTransaction.id:
            return True
        return False
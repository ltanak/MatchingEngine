import random
import numpy as np
import heapq
import time
import math
import uuid

class Transaction:

    def __init__(self, fromCSV = [], generate = False): # Initialises variables, can either input as CSV or generate order
        self.timestamp = -1
        self.id = -1
        self.type = None
        self.price = -1
        self.quantity = -1
        if len(fromCSV) != 0:
            self.createTransactionCSV(fromCSV)
        elif generate:
            self.generateOrder()

    def getPrice(self):
        return self.price
    
    def getQuantity(self):
        return self.quantity

    def generateOrder(self):
        self.timestamp = time.time()
        self.id = uuid.uuid4()
        self.price = random.randint(1, 100)
        self.quantity = random.randint(1, 10)
        if random.randint(1,2) == 1:
            self.type == "BID"
        else:
            self.type == "ASK"

    # Creates transaction from CSV input

    def createTransactionCSV(self, csvInputArray):
        self.timestamp = float(csvInputArray[0]) # cahgehsghsklfjsdaklllllllllllllllllllllll
        self.id = int(csvInputArray[2])
        self.quantity = float(csvInputArray[3])
        self.price = float(csvInputArray[4])
        if csvInputArray[5] == "1":
            self.type = "BID"
        else:
            self.type = "ASK"

    # Sets transaction to input paramters, generates ID if not supplied

    def setTransaction(self, timestamp, type, price, quantity, id = -1):
        self.timestamp = timestamp
        self.type = type
        self.price = price
        self.quantity = quantity
        self.id = id
        if id == -1:
            self.id = uuid.uuid4()

    def reduceQuantity(self, value):
        self.quantity -= value

    """
    Comparison Functions - implemented due to app crashing when comparing objects
    - Cannot do by volume as volumes may also be the same
    - Comparing transaction id as they are unique
    - Larger number / id means more bits meaning more computation
    """

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
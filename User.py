from collections import deque
import random
import numpy as np
import heapq
import time
import math
import uuid
from Transaction import Transaction

"""
User class to store relevant information for their orders
"""

class User():

    def __init__(self, accountBalance):
        self.orderHistory = [] # Stores Transactions
        self.liveOrders = {}
        self.orderQueue = deque() # Queue implementation for pending orders
        self.startBalance = accountBalance
        self.accountBalance = accountBalance
        self.totalOrderValues = 0
        self.stockBoughtAt = 0
        self.totalOrderVolume = 0
        self.currentPL = 0

    # If order is valid, add to queue

    def placeOrder(self, inputOrder: Transaction):
        res = self.updateValues(inputOrder)
        if res:
            self.orderHistory.append(inputOrder)
            self.orderQueue.append(inputOrder)

    def addLiveOrder(self, inputOrder: Transaction):
        self.liveOrders[inputOrder.id] = inputOrder

    def removeLiveOrder(self, id):
        del self.liveOrders[id]

    # If order violates balance constraints, return False

    def updateValues(self, inputOrder: Transaction):
        priceBought = inputOrder.getPrice()
        totalAmountBought = inputOrder.getQuantity() * priceBought

        if inputOrder.type == "BID":
            if self.accountBalance - totalAmountBought < 0:
                return False
        
        self.stockBoughtAt = priceBought
        factor = 1
        if inputOrder.type == "BID":
            factor = -1

        self.totalOrderVolume += (inputOrder.getQuantity() * -1 * factor) # Reduce or increase current order count accordingly
        self.totalOrderValues -= (factor * totalAmountBought) # Reduce or increase total order value accordingly
        self.accountBalance += (factor * totalAmountBought) # Reduce or increase balance accordingly

        if self.totalOrderVolume == 0: # If no more orders, calculate P&L
            self.neutral()
        return True

    def isWaiting(self): # Check if order waiting in queue
        if len(self.orderQueue) == 0:
            return False
        return True

    def popOrderQueue(self): # Retrieve transaction from queue
        transaction = self.orderQueue.popleft()
        return transaction
    
    def isUserOrder(self, id): # Check if it is a user order
        if id in self.liveOrders:
            return True
        return False
    
    def neutral(self): # Calculate P&L
        self.currentPL = self.accountBalance - self.startBalance
        self.totalOrderValues = 0
        self.stockBoughtAt = 0
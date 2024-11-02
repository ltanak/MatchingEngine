from collections import deque
import random
import numpy as np
import heapq
import time
import math
import uuid
from Transaction import Transaction

class User():

    def __init__(self, accountBalance):
        self.orderHistory = [] # Stores Transaction.py
        self.liveOrders = {}
        self.orderQueue = deque()
        self.startBalance = accountBalance
        self.accountBalance = accountBalance
        self.totalOrderValues = 0
        self.stockBoughtAt = 0
        self.totalOrderVolume = 0
        self.currentPL = 0

    def placeOrder(self, inputOrder: Transaction):
        res = self.updateValues(inputOrder)
        if res:
            self.orderHistory.append(inputOrder)
            self.orderQueue.append(inputOrder)

    def addLiveOrder(self, inputOrder: Transaction):
        self.liveOrders[inputOrder.id] = inputOrder

    def removeLiveOrder(self, id):
        del self.liveOrders[id]

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

        self.totalOrderVolume += (inputOrder.getQuantity() * -1 * factor)
        self.totalOrderValues -= (factor * totalAmountBought)
        self.accountBalance += (factor * totalAmountBought)

        if self.totalOrderVolume == 0:
            self.neutral()
        return True

    def isWaiting(self):
        if len(self.orderQueue) == 0:
            return False
        return True

    def popOrderQueue(self):
        transaction = self.orderQueue.popleft()
        return transaction
    
    def isUserOrder(self, id):
        if id in self.liveOrders:
            return True
        return False
    
    def neutral(self):
        self.currentPL = self.accountBalance - self.startBalance
        self.totalOrderValues = 0
        self.stockBoughtAt = 0
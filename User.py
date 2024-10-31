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
        self.totalOrderVolume = 0
        self.currentPL = 0

    def placeOrder(self, inputOrder: Transaction):
        self.orderHistory.append(inputOrder)
        self.orderQueue.append(inputOrder)
        self.updateValues(inputOrder)

    def addLiveOrder(self, inputOrder: Transaction):
        self.liveOrders[inputOrder.id] = inputOrder

    def removeLiveOrder(self, id):
        del self.liveOrders[id]

    def updateValues(self, inputOrder: Transaction):
        factor = 1
        if inputOrder.type == "BID":
            factor = -1
        value = inputOrder.getPrice()
        self.totalOrderVolume += (inputOrder.getQuantity() * -1 * factor)
        self.totalOrderValues -= (factor * value * inputOrder.getQuantity())
        if self.totalOrderVolume == 0:
            self.totalOrderValues = 0
        self.accountBalance += (factor * value * inputOrder.getQuantity())
        self.currentPL = self.accountBalance - self.startBalance

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
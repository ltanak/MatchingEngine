from Transaction import Transaction
import heapq

class MatchingEngine:
    
    def __init__(self):
        self.buyBook = []   # Both are arrays that will be implemented / used with heapq library
        self.sellBook = [] 
        self.orderMap = {}  # Tracks ids of all live orders
        tempTransaction = Transaction()
        tempTransaction.setTransaction(-1, "BID", -1, -1) # Sets temporary transaction for the first match
        self.mostRecentMatch = [tempTransaction, tempTransaction]

    def addToBook(self, transaction: Transaction): # Adds transaction to corresponding book
        self.orderMap[transaction.id] = transaction
        if transaction.type == "BID":
            valueToInsert = [transaction.price * -1, transaction.timestamp, transaction] # As using max-heap, must multiply by -1
            heapq.heappush(self.buyBook, valueToInsert)
        else:
            valueToInsert = [transaction.price, transaction.timestamp, transaction]
            heapq.heappush(self.sellBook, valueToInsert)

    def popFromBuy(self): # Remove the transaction from the buy book, also remove from map
        transaction = heapq.heappop(self.buyBook)
        transaction[0] *= -1
        if transaction[2].id in self.orderMap:
            del self.orderMap[transaction[2].id]
        return transaction
    
    def popFromSell(self): # Remove the transaction from the sell book, also remove from map
        transaction = heapq.heappop(self.sellBook)
        if transaction[2].id in self.orderMap:
            del self.orderMap[transaction[2].id]
        return transaction
    
    def printBooks(self): # prints all values from books
        print(f"BUY BOOK: {self.buyBook}")
        print(f"SELL BOOK: {self.sellBook}")
    
    def getOrderFromId(self, id): # checks if id correponsds to a transaction
        if id in self.orderMap:
            return self.orderMap[id]
        return -1
    
    def tradeMatched(self, buyTransaction: Transaction, sellTransaction: Transaction): # Sets most recent trade match to input parameters
        self.mostRecentMatch = [buyTransaction, sellTransaction]

    def getMostRecentMatch(self):
        return self.mostRecentMatch
    
    """
    Price time priority algorithm
    Returns True / False if trade was successfully processed
    If max of buy book is less then min of sell, ignore
    Otherwise, reduce quantities accordingly and if needed add updated transaction to 
    corresponding book
    """

    def priceTimePriority(self):
        if not self.buyBook or not self.sellBook:
            return False
        
        # Values from heap stored as (price, timestamp, Transaction())

        currentBuy = self.buyBook[0]
        currentSell = self.sellBook[0]
        if currentBuy[0] * -1 < currentSell[0]:
            return False
        else:
            currentBuy = self.popFromBuy()
            currentSell = self.popFromSell()

            buyQuantity = currentBuy[2].quantity
            sellQuantity = currentSell[2].quantity

            if buyQuantity == sellQuantity:
                self.tradeMatched(currentBuy[2], currentSell[2]) # If volumes same, neither added back
                return True
            elif buyQuantity > sellQuantity:
                currentBuy[2].reduceQuantity(sellQuantity)
                self.addToBook(currentBuy[2])
                self.tradeMatched(currentBuy[2], currentSell[2]) # If more buy orders, reduce volume by amount matched, add back to book
                return True
            else:
                currentSell[2].reduceQuantity(buyQuantity)
                self.addToBook(currentSell[2])
                self.tradeMatched(currentBuy[2], currentSell[2]) # If more sell orders, reduce volume by amount matched, add back to book
                return True

    def proRata(self):
        if not self.buyBook or not self.sellBook:
            return False
        return True
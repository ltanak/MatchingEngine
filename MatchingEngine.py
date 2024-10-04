from Transaction import Transaction
import heapq

class MatchingEngine:
    
    def __init__(self):
        self.buyBook = []   # Both are arrays that will be using heapq
        self.sellBook = []  # 

    def addToBook(self, transaction: Transaction):
        if transaction.type == "BID":
            valueToInsert = (transaction.price * -1, transaction.timestamp, transaction)
            heapq.heappush(self.buyBook, valueToInsert)
        else:
            valueToInsert = (transaction.price, transaction.timestamp, transaction)
            heapq.heappush(self.sellBook, valueToInsert)

    def popFromBuy(self):
        transaction = heapq.heappop(self.buyBook)
        transaction[0] *= -1
        return transaction
    
    def popFromSell(self):
        transaction = heapq.heappop(self.sellBook)
        return transaction
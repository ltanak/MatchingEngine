from Transaction import Transaction
import heapq

class MatchingEngine:
    
    def __init__(self):
        self.buyBook = []   # Both are arrays that will be using heapq
        self.sellBook = []  # 
        self.orderMap = {}

    def addToBook(self, transaction: Transaction):
        self.orderMap[transaction.id] = transaction
        if transaction.type == "BID":
            valueToInsert = [transaction.price * -1, transaction.timestamp, transaction]
            heapq.heappush(self.buyBook, valueToInsert)
        else:
            valueToInsert = [transaction.price, transaction.timestamp, transaction]
            heapq.heappush(self.sellBook, valueToInsert)

    def popFromBuy(self):
        transaction = heapq.heappop(self.buyBook)
        transaction[0] *= -1
        if transaction[2].id in self.orderMap:
            del self.orderMap[transaction[2].id]
        return transaction
    
    def popFromSell(self):
        transaction = heapq.heappop(self.sellBook)
        if transaction[2].id in self.orderMap:
            del self.orderMap[transaction[2].id]
        return transaction
    
    def printBooks(self):
        print(f"BUY BOOK: {self.buyBook}")
        print(f"SELL BOOK: {self.sellBook}")
    
    def getOrderFromId(self, id):
        if id in self.orderMap:
            return self.orderMap[id]
        return -1
    
    def tradeMatched(self, buyTransaction, sellTransaction, quantity):
        return
        # print(f"Trade matched at price: {buyTransaction[0]}, volume: {quantity}. BuyID: {buyTransaction[2].id}, SellID: {sellTransaction[2].id} EOL")

    def priceTimePriority(self):
        if not self.buyBook or not self.sellBook:
            return False
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
                self.tradeMatched(currentBuy, currentSell, buyQuantity)
                return True
            elif buyQuantity > sellQuantity:
                currentBuy[2].reduceQuantity(sellQuantity)
                self.addToBook(currentBuy[2])
                self.tradeMatched(currentBuy, currentSell, sellQuantity)
                return True
            else:
                currentSell[2].reduceQuantity(buyQuantity)
                self.addToBook(currentSell[2])
                self.tradeMatched(currentBuy, currentSell, buyQuantity)
                return True

    def proRata(self):
        if not self.buyBook or not self.sellBook:
            return False
        return True
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
    
    def tradeMatched(self, buyTransaction, sellTransaction, quantity):
        print(f"Trade matched at price: f{buyTransaction[0]}, volume: f{quantity}. BuyID: f{buyTransaction[2].id}, SellID: f{sellTransaction[2].id}")

    def priceTimePriority(self):
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
                self.addToBook(currentBuy)
                self.tradeMatched(currentBuy, currentSell, sellQuantity)
                return True
            else:
                currentSell[2].reduceQuantity(buyQuantity)
                self.addToBook(currentSell)
                self.tradeMatched(currentBuy, currentSell, buyQuantity)
                return True

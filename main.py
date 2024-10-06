from MatchingEngine import MatchingEngine
from Transaction import Transaction
import time
import uuid
# a = Transaction(timestamp = 1, price = 50, quantity = 1)
# b = Transaction(timestamp = 2, price = 40, quantity = 90)
# c = Transaction(timestamp = 5, price = 50, quantity = 1)
# d = Transaction(timestamp = 6, price = 100, quantity = 1)

# engine = MatchingEngine()

# engine.addToBuyBook(a)
# engine.addToBuyBook(b)
# print(engine.buyBook)

if __name__ == "__main__":
    engine = MatchingEngine()
    while True:
        price = int(input("Enter price: "))
        quantity = int(input("Quantity: "))
        orderType = str(input("Order type: "))
        transaction = Transaction(timestamp=time.time(), id = uuid.uuid4(), type = orderType, price = price, quantity = quantity)
        engine.addToBook(transaction)
        engine.printBooks()
        print("--------------")
        matched = engine.priceTimePriority()
        while matched:
            matched = engine.priceTimePriority()
        print("--------------")
        engine.printBooks()
        print("--------------")
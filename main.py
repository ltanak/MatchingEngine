from MatchingEngine import MatchingEngine
from Transaction import Transaction
import time
import uuid
import csv
import os
# a = Transaction(timestamp = 1, price = 50, quantity = 1)
# b = Transaction(timestamp = 2, price = 40, quantity = 90)
# c = Transaction(timestamp = 5, price = 50, quantity = 1)
# d = Transaction(timestamp = 6, price = 100, quantity = 1)

# engine = MatchingEngine()

# engine.addToBuyBook(a)
# engine.addToBuyBook(b)
# print(engine.buyBook)

dataSource = "Resources/MSFT1/"
fileToOpen = dataSource + "MSFTBook.csv"

if __name__ == "__main__":
    engine = MatchingEngine()
    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")
        for row in spamreader:
            row = list(row)
            time.sleep(0.2)
            if row[1] == "1":
                transaction = Transaction(fromCSV = row)
                engine.addToBook(transaction)
                matched = engine.priceTimePriority()
                while matched:
                    matched = engine.priceTimePriority()

    # while True:
    #     price = int(input("Enter price: "))
    #     quantity = int(input("Quantity: "))
    #     orderType = str(input("Order type: "))
    #     transaction = Transaction(timestamp=time.time(), id = uuid.uuid4(), type = orderType, price = price, quantity = quantity)
    #     engine.addToBook(transaction)
    #     engine.printBooks()
    #     print("--------------")
    #     matched = engine.priceTimePriority()
    #     while matched:
    #         matched = engine.priceTimePriority()
    #     print("--------------")
    #     engine.printBooks()
    #     print("--------------")
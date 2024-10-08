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
            if row[1] == "1":
                transaction = Transaction(fromCSV = row)
                engine.addToBook(transaction)
                matched = engine.priceTimePriority()
                while matched:
                    matched = engine.priceTimePriority()

        # To do -
        # - add case where if we have matching price and matching ID and timestamp, it will not execute trade
        # - clean up output to make it nicer to show trades matching
        # - record which transactions have occurred for P/L
        # - implement other types of algorithms
        # - work on implementing web app to place trades as a user as well

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
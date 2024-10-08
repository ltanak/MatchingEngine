from MatchingEngine import MatchingEngine
from Transaction import Transaction
import time
import uuid
import csv
import os
import matplotlib as mpl
from plotting import Plotting

dataSource = "Resources/MSFT1/"
fileToOpen = dataSource + "MSFTBook.csv"

if __name__ == "__main__":
    engine = MatchingEngine()
    plot = Plotting()
    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")
        startTime = time.time()
        for row in spamreader:
            row = list(row)
            if row[1] == "1":
                transaction = Transaction(fromCSV = row)
                engine.addToBook(transaction)
                matched = engine.priceTimePriority()
                while matched:
                    plot.add(time.time() - startTime, transaction.price)
                    matched = engine.priceTimePriority()
    plot.plot()

        # To do -
        # - add case where if we have matching price and matching ID and timestamp, it will not execute trade
        # - clean up output to make it nicer to show trades matching
        # - record which transactions have occurred for P/L
        # - implement other types of algorithms
        # - work on implementing web app to place trades as a user as well

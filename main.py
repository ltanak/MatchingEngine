from MatchingEngine import MatchingEngine
from Transaction import Transaction
from TradedEngine import TradedEngine
import time
import uuid
import csv
import os
import matplotlib as mpl
from plotting import Plotting

dataSource = "Resources/MSFT1/"
fileToOpen = dataSource + "MSFTBook.csv"

"""
Initial testing for matching engine
Loops over values in dataset, if valid performs matching algorithm on it
Continues until dataset is finished
"""

if __name__ == "__main__":
    engine = MatchingEngine()
    plot = Plotting(fileInput=fileToOpen)
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
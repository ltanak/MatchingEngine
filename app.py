import threading
from flask import *
import json
import time
import random
from MatchingEngine import MatchingEngine
from Transaction import Transaction
import uuid
import csv
import os
import matplotlib as mpl
from plotting import Plotting
from decimal import Decimal

app = Flask(__name__)

LOCALSTARTTIME = time.time()
THREADENABLED = True

def background():
    dataSource = "Resources/MSFT1/"
    fileToOpen = dataSource + "MSFTBook.csv"
    currentTradedValue = None
    engine = MatchingEngine()

    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for row in spamreader:
            if not THREADENABLED:
                break
            else:
                time.sleep(0.2)
                row = list(row)
                if row[1] == "1":
                    transaction = Transaction(fromCSV = row)
                    engine.addToBook(transaction)
                    matched = engine.priceTimePriority()
                    while matched:
                        # plot.add(time.time() - startTime, transaction.price)
                        currentTradedValue = transaction.price
                        print(time.time() - LOCALSTARTTIME, transaction.price)
                        matched = engine.priceTimePriority()
            # Send (currentTradedValue, time.time() - startTime) to frontend


    return
    
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = [(time.time() - LOCALSTARTTIME) * 1000, -1]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData(transactionPrice):
    data = [(time.time() - LOCALSTARTTIME) * 1000, transactionPrice]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

# @app.route('/tradingValue', methods=['GET','POST'])
# def tradingValue(newPrice = None):
#     if not newPrice:
        



if __name__ == '__main__':
    trading = threading.Thread(target=background).start()
    app.run(debug=True, threaded=True)
    THREADENABLED = False
    trading.join()
    exit(0)

# TO-DO List for soon
# - Make API call when trade is matched
# - API call is a "broadcast"
# - JS is an async that listens out for this broadcast
# - Plots new point on graph
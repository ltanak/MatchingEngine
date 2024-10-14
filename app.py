import threading
from flask import *
import random
import json
import time
from random import random
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

    engine = MatchingEngine()

    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for row in spamreader:
            if THREADENABLED:
                time.sleep(0.2)
                row = list(row)
                if row[1] == "1":
                    transaction = Transaction(fromCSV = row)
                    engine.addToBook(transaction)
                    matched = engine.priceTimePriority()
                    while matched:
                        # plot.add(time.time() - startTime, transaction.price)
                        print(time.time() - LOCALSTARTTIME, transaction.price)
                        matched = engine.priceTimePriority()
            else:
                break
    return
    
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = [(time.time() - LOCALSTARTTIME) * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData(transactionPrice):
    data = [(time.time() - LOCALSTARTTIME) * 1000, transactionPrice]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

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
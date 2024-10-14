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

def background():
    dataSource = "Resources/MSFT1/"
    fileToOpen = dataSource + "MSFTBook.csv"

    engine = MatchingEngine()

    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")
        startTime = time.time()  
        for row in spamreader:
            time.sleep(0.2)
            row = list(row)
            if row[1] == "1":
                transaction = Transaction(fromCSV = row)
                engine.addToBook(transaction)
                matched = engine.priceTimePriority()
                while matched:
                    # plot.add(time.time() - startTime, transaction.price)
                    print(time.time() - startTime, transaction.price)
                    matched = engine.priceTimePriority()
    return "fin"
    
@app.route('/', methods=["GET", "POST"])
def main():
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = [time.time() * 1000, random() * 100]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData(transactionPrice):
    data = [time.time(), transactionPrice]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

if __name__ == '__main__':
    trading = threading.Thread(target=background)
    trading.start()
    app.run(debug=True, threaded=True)
    trading.kill()
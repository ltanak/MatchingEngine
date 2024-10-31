import threading
from flask import *
import json
import time
import random
from MatchingEngine import MatchingEngine
from Transaction import Transaction
from TradedEngine import TradedEngine
from User import User
import uuid
import csv
import os
import matplotlib as mpl
from plotting import Plotting
from decimal import Decimal

app = Flask(__name__)

LOCALSTARTTIME = time.time()
THREADENABLED = True
TRADEDENGINE = TradedEngine()
USER = User(accountBalance = 1000000)

def background():
    dataSource = "Resources/MSFT1/"
    fileToOpen = dataSource + "MSFTBook.csv"
    engine = MatchingEngine()

    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for row in spamreader:
            if THREADENABLED:
                time.sleep(0.2)
                if USER.isWaiting():
                    userTransaction = USER.popOrderQueue()
                    USER.addLiveOrder(userTransaction)
                    matching(engine= engine, transaction= userTransaction)

                row = list(row)
                if row[1] == "1":
                    newTransaction = Transaction(fromCSV= row)
                    matching(engine= engine, transaction= newTransaction)
    return -1

def matching(engine: MatchingEngine, transaction: Transaction):
    volatility = random.randint(-99, 99)
    transaction.price += volatility
    engine.addToBook(transaction)
    matchedPair = engine.getMostRecentMatch()
    matched = engine.priceTimePriority()
    while matched:
        newVolume = transaction.quantity if transaction.type == "BID" else -transaction.quantity
        TRADEDENGINE._updateAll(transaction.price, (time.time() - LOCALSTARTTIME) * 100, newVolume)
        print(time.time() - LOCALSTARTTIME, transaction.price)

        matchedPair = engine.getMostRecentMatch()
        checkUser(engine, matchedPair[0])
        checkUser(engine, matchedPair[1])

        matched = engine.priceTimePriority()
    
    checkUser(engine, matchedPair[0])
    checkUser(engine, matchedPair[1])

    TRADEDENGINE._updateTime((time.time() - LOCALSTARTTIME) * 100)

def checkUser(engine, transaction):
    if USER.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            USER.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            USER.updateValues(transaction)
    return

@app.route('/', methods=["GET", "POST"])
def main():
    if request.method == 'POST':
        volume = request.form['volume']
        print(volume)
        orderType = request.form['orderType']    
        print(orderType)
        userTransaction = Transaction()
        userTransaction.setTransaction(time.time() - LOCALSTARTTIME, orderType, TRADEDENGINE.getCurrentPrice(), float(volume))
        USER.placeOrder(userTransaction)
    return render_template('index.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    data = [(time.time() - LOCALSTARTTIME), -1]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData():
    data = [TRADEDENGINE.getMostRecentTimestamp(), TRADEDENGINE.getCurrentPrice()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/tradingValue')
def tradingInformation():
    # data = TRADEDENGINE.getCurrentPrice()
    # response = make_response(json.dumps(data))
    # response.content_type = 'application/json'
    return jsonify(price = TRADEDENGINE.getCurrentPrice(), volume = TRADEDENGINE.getCurrentVolume(), userPrice = USER.accountBalance, userValue = USER.totalOrderValues, userStock = USER.totalOrderVolume, PL = USER.currentPL)

@app.route('/userPlaceOrder', methods=["POST"])
def userPlaceOrder():
    if request.method == 'POST':
        volume = request.form['volume']
        print(volume)
        orderType = request.form['orderType']    
        print(orderType)
        userTransaction = Transaction()
        userTransaction.setTransaction(time.time() - LOCALSTARTTIME, orderType, TRADEDENGINE.getCurrentPrice(), float(volume))
        USER.placeOrder(userTransaction)
    return
    
if __name__ == '__main__':
    trading = threading.Thread(target=background).start()
    app.run(debug=True, threaded=True)
    THREADENABLED = False
    trading.join()
    exit(0)

"""
TO DO -
- Add buttons for inputting a trade
    - Input volume
    - input order (BUY or SELL)
- On serverside, store a hashmap with users ID?
- Or store individual class that keeps track of their trades
    - Class stores all different stocks
    - Array of order classes / transaction?
- When they input trade, goes into matching engine - DONE
- When it is matched, updates class (which contents are displayed on FE)
- do same method of other APIs

- Figure out how to do the page switching
- Update stock volume to be the amount of stocks being traded, 
not most recent trade stock


"""
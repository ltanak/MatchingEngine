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
from Portfolio import Portfolio

app = Flask(__name__)

LOCALSTARTTIME = time.time()
THREADENABLED = True
TRADEDENGINE = TradedEngine()
USER = User(accountBalance = 1000000)

MSFTACCOUNT = User(accountBalance = 1000000)
AMZNACCOUNT = User(accountBalance = 1000000)
GOOGACCOUNT = User(accountBalance = 1000000)
AAPLACCOUNT = User(accountBalance = 1000000)
INTCACCOUNT = User(accountBalance = 1000000)

STOCKSLIST = [MSFTACCOUNT, AAPLACCOUNT, AMZNACCOUNT, GOOGACCOUNT, INTCACCOUNT]

PORTFOLIO = Portfolio(STOCKSLIST)

def background(dataSource, stock):
    fileToOpen = dataSource
    engine = MatchingEngine()
    accountType = PORTFOLIO.getAccount(stock)
    with open(fileToOpen, newline = "") as csvfile:
        spamreader = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for row in spamreader:
            if THREADENABLED:
                time.sleep(0.2)
                if accountType.isWaiting():
                    userTransaction = accountType.popOrderQueue()
                    accountType.addLiveOrder(userTransaction)
                    matching(engine= engine, transaction= userTransaction, stock= stock)

                row = list(row)
                if row[1] == "1":
                    newTransaction = Transaction(fromCSV= row)
                    matching(engine= engine, transaction= newTransaction, stock= stock)
    return -1

def matching(engine: MatchingEngine, transaction: Transaction, stock):
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
        checkUser(engine, matchedPair[0], stock)
        checkUser(engine, matchedPair[1], stock)

        matched = engine.priceTimePriority()
    
    checkUser(engine, matchedPair[0], stock)
    checkUser(engine, matchedPair[1], stock)

    TRADEDENGINE._updateTime((time.time() - LOCALSTARTTIME) * 100)

def checkUser(engine, transaction, stock):
    account = PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)
    return

@app.route('/index.html', methods=["GET", "POST"])
def main():
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
    accountType = PORTFOLIO.getAccount("MSFT")
    return jsonify(
        price = TRADEDENGINE.getCurrentPrice(), 
        userPrice = accountType.accountBalance, 
        userValue = accountType.stockBoughtAt, 
        userStock = accountType.totalOrderVolume, 
        PL = accountType.currentPL)

@app.route('/userPlaceOrder', methods=["POST"])
def userPlaceOrder():
    if request.method == 'POST':
        volume = request.form['volume']
        orderType = request.form['orderType']    
        userTransaction = Transaction()
        userTransaction.setTransaction(time.time() - LOCALSTARTTIME, orderType, TRADEDENGINE.getCurrentPrice(), float(volume))
        accountType = PORTFOLIO.getAccount("MSFT")
        accountType.placeOrder(userTransaction)
    return "Trade submitted"
    
if __name__ == '__main__':
    trading = threading.Thread(target=background, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"]).start()
    app.run(debug=True, threaded=True)
    THREADENABLED = False
    trading.join()
    exit(0)

"""
TO DO -
- Or store individual class that keeps track of their trades
    - Class stores all different stocks
    - Array of order classes / transaction?
- When it is matched, updates class (which contents are displayed on FE)
- do same method of other APIs
- Display percentage of buy vs sell orders
- Figure out how to do the page switching
    - Store either different types of books, or create multiple objects
    - User has different wallets? - or user stores different stocks info in array or map
    - make it so that chart preloads all data that is stored for the image - make it keep track of all points / trades matched

"""
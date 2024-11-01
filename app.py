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
from TradedEngineCollection import TradedEngineCollection

app = Flask(__name__)

LOCALSTARTTIME = time.time()
THREADENABLED = True

MSFT_ENGINE = TradedEngine()
AAPL_ENGINE = TradedEngine()
AMZN_ENGINE = TradedEngine()
GOOG_ENGINE = TradedEngine()
INTC_ENGINE = TradedEngine()

STOCK_ENGINES = [MSFT_ENGINE, AAPL_ENGINE, AMZN_ENGINE, GOOG_ENGINE, INTC_ENGINE]

MSFT_ACCOUNT = User(accountBalance = 1000000)
AMZN_ACCOUNT = User(accountBalance = 1000000)
GOOG_ACCOUNT = User(accountBalance = 1000000)
AAPL_ACCOUNT = User(accountBalance = 1000000)
INTC_ACCOUNT = User(accountBalance = 1000000)

STOCKS_LIST = [MSFT_ACCOUNT, AAPL_ACCOUNT, AMZN_ACCOUNT, GOOG_ACCOUNT, INTC_ACCOUNT]

PORTFOLIO = Portfolio(STOCKS_LIST)
ENGINE_COLLECTION = TradedEngineCollection(STOCK_ENGINES)

def background(dataSource, stock):
    engine = MatchingEngine()
    accountType = PORTFOLIO.getAccount(stock)
    with open(dataSource, newline = "") as csvfile:
        file = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for row in file:
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
    stockEngine = ENGINE_COLLECTION.getEngine(stock)

    volatility = random.randint(-99, 99)
    transaction.price += volatility
    engine.addToBook(transaction)
    matchedPair = engine.getMostRecentMatch()
    matched = engine.priceTimePriority()
    while matched:
        newVolume = transaction.quantity if transaction.type == "BID" else -transaction.quantity
        stockEngine._updateAll(transaction.price, (time.time() - LOCALSTARTTIME) * 100, newVolume)
        print(f"{stock}: {time.time() - LOCALSTARTTIME} , {transaction.price}")

        matchedPair = engine.getMostRecentMatch()
        checkUser(engine, matchedPair[0], stock)
        checkUser(engine, matchedPair[1], stock)

        matched = engine.priceTimePriority()
    
    checkUser(engine, matchedPair[0], stock)
    checkUser(engine, matchedPair[1], stock)

    stockEngine._updateTime((time.time() - LOCALSTARTTIME) * 100)

def checkUser(engine, transaction, stock):
    account = PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)
    return;

@app.route('/index.html', methods=["GET", "POST"])
def main():
    return render_template('index.html')

# THIS FUNCTION HERE REQUIRES CHANGING TO MAKE IT APPLICABLE TO ALL DIFFERENT STOCKS

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData():
    stockEngine = ENGINE_COLLECTION.getEngine("MSFT")
    data = [stockEngine.getMostRecentTimestamp(), stockEngine.getCurrentPrice()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

# THIS FUNCTION HERE REQUIRES CHANGING TO MAKE IT APPLICABLE TO ALL DIFFERENT STOCKS

@app.route('/tradingValue')
def tradingInformation():
    accountType = PORTFOLIO.getAccount("MSFT")
    stockEngine = ENGINE_COLLECTION.getEngine("MSFT")
    return jsonify(
        price = stockEngine.getCurrentPrice(), 
        userPrice = accountType.accountBalance, 
        userValue = accountType.stockBoughtAt, 
        userStock = accountType.totalOrderVolume, 
        PL = accountType.currentPL)

# THIS FUNCTION HERE REQUIRES CHANGING TO MAKE IT APPLICABLE TO ALL DIFFERENT STOCKS

@app.route('/userPlaceOrder', methods=["POST"])
def userPlaceOrder():
    if request.method == 'POST':
        stockEngine = ENGINE_COLLECTION.getEngine("MSFT")
        accountType = PORTFOLIO.getAccount("MSFT") # THESE NEEDS TO CHANGE HERE - MAKE API SEND WHICH ONE TO USE
        volume = request.form['volume']
        orderType = request.form['orderType']    
        userTransaction = Transaction()
        userTransaction.setTransaction(time.time() - LOCALSTARTTIME, orderType, stockEngine.getCurrentPrice(), float(volume))
        accountType.placeOrder(userTransaction)
    return "Trade submitted"
    
if __name__ == '__main__':
    MSFT = threading.Thread(target=background, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"]).start()
    AAPL = threading.Thread(target=background, args=["Resources/AAPL1/AAPLBook.csv", "AAPL"]).start()
    app.run(debug=True, threaded=True)
    THREADENABLED = False
    MSFT.join()
    AAPL.join()
    exit(0)
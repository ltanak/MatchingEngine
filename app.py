import threading
from flask import *
from flask.globals import request
import json
import time
import random
from MatchingEngine import MatchingEngine
from Transaction import Transaction
from TradedEngine import TradedEngine
from User import User
import csv
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

STOCK_ENGINES = {"MSFT": MSFT_ENGINE, 
             "AAPL": AAPL_ENGINE, 
             "AMZN": AMZN_ENGINE,
             "GOOG": GOOG_ENGINE,
             "INTC": INTC_ENGINE}

MSFT_ACCOUNT = User(accountBalance = 1000000)
AMZN_ACCOUNT = User(accountBalance = 1000000)
GOOG_ACCOUNT = User(accountBalance = 1000000)
AAPL_ACCOUNT = User(accountBalance = 1000000)
INTC_ACCOUNT = User(accountBalance = 1000000)

STOCK_ACCOUNTS = {"MSFT": MSFT_ACCOUNT, "AAPL": AAPL_ACCOUNT, "AMZN": AMZN_ACCOUNT, "GOOG": GOOG_ACCOUNT, "INTC": INTC_ACCOUNT}

PORTFOLIO = Portfolio(STOCK_ACCOUNTS)
ENGINE_COLLECTION = TradedEngineCollection(STOCK_ENGINES)

"""
Initialises engine and selects user account for specific stock.
Loops over specified dataset
If user transaction queued, call matching function on it
If dataset transaction valid, call matching function on it
"""

def transactionLoop(dataSource: str, stock: str):
    engine = MatchingEngine()
    accountType = PORTFOLIO.getAccount(stock)
    with open(dataSource, newline = "") as csvfile:
        file = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for data in file:
            if not THREADENABLED:
                break
            else:
                time.sleep(0.2)
                if accountType.isWaiting():
                    userTransaction = accountType.popOrderQueue()
                    accountType.addLiveOrder(userTransaction)
                    matching(engine, userTransaction, stock)

                data = list(data)
                if data[1] == "1":
                    newTransaction = Transaction(fromCSV= data)
                    matching(engine, newTransaction, stock)
    return -1

def matching(engine: MatchingEngine, transaction: Transaction, stock):
    stockEngine = ENGINE_COLLECTION.getEngine(stock)

    transaction.price = int(transaction.price * (1 + random.uniform(-0.1, 0.1)))

    engine.addToBook(transaction)
    matchedPair = engine.getMostRecentMatch()
    matched = engine.priceTimePriority()
    if not matched:
        for order in matchedPair:
            checkUser(engine, order, stock)

    while matched:
        newVolume = transaction.quantity if transaction.type == "BID" else -transaction.quantity
        stockEngine._updateAll(transaction.price, (time.time() - LOCALSTARTTIME) * 100, newVolume)
        print(f"{stock}: {time.time() - LOCALSTARTTIME} , {transaction.price}")

        matchedPair = engine.getMostRecentMatch()
        for order in matchedPair:
            checkUser(engine, order, stock)

        matched = engine.priceTimePriority()
    

    if stockEngine.getCurrentPrice() != None:
        stockEngine._updateAll(stockEngine.getCurrentPrice(), (time.time() - LOCALSTARTTIME) * 100, stockEngine.getCurrentVolume())

def checkUser(engine: MatchingEngine, transaction: Transaction, stock: str):
    account = PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)

@app.route('/', methods=["GET", "POST"])
def main():
    return redirect('/msft.html')

@app.route('/msft.html', methods=["GET", "POST"])
def msft():
    return render_template('msft.html')

@app.route('/aapl.html', methods=["GET", "POST"])
def aapl():
    return render_template('aapl.html')

@app.route('/amzn.html', methods=["GET", "POST"])
def amzn():
    return render_template('amzn.html')

@app.route('/goog.html', methods=["GET", "POST"])
def goog():
    return render_template('goog.html')

@app.route('/intc.html', methods=["GET", "POST"])
def intc():
    return render_template('intc.html')

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData():
    stock = request.args.get('stockType')

    stockEngine = ENGINE_COLLECTION.getEngine(stock)
    data = [stockEngine.getMostRecentTimestamp(), stockEngine.getCurrentPrice()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

@app.route('/tradingValue', methods=["GET", "POST"])
def tradingInformation():
    stock = request.args.get('stock')
    accountType = PORTFOLIO.getAccount(stock)
    stockEngine = ENGINE_COLLECTION.getEngine(stock)
    return jsonify(
        price = stockEngine.getCurrentPrice(), 
        userPrice = accountType.accountBalance, 
        userValue = accountType.stockBoughtAt, 
        userStock = accountType.totalOrderVolume, 
        PL = accountType.currentPL)

@app.route('/preloadData', methods=["GET", "POST"])
def preloadData():
    stock = request.args.get('stock')
    engine = STOCK_ENGINES[stock]
    pricesArray = engine.getAllPrices()
    timestampsArray = engine.getAllTimestamps()
    return jsonify(
        prices = pricesArray,
        timestamps = timestampsArray
    )

@app.route('/userPlaceOrder', methods=["POST"])
def userPlaceOrder():
    if request.method == 'POST':
        stock = request.form['stock']

        stockEngine = ENGINE_COLLECTION.getEngine(stock)
        accountType = PORTFOLIO.getAccount(stock)

        volume = request.form['volume']
        orderType = request.form['orderType']    
        userTransaction = Transaction()
        userTransaction.setTransaction(time.time() - LOCALSTARTTIME, orderType, stockEngine.getCurrentPrice(), float(volume))
        accountType.placeOrder(userTransaction)
    return "Trade submitted"
    
if __name__ == '__main__':

    STOCK_THREADS = [
        threading.Thread(target=transactionLoop, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"]),
        threading.Thread(target=transactionLoop, args=["Resources/AAPL1/AAPLBook.csv", "AAPL"]),
        threading.Thread(target=transactionLoop, args=["Resources/AMZN1/AMZNBook.csv", "AMZN"]),
        threading.Thread(target=transactionLoop, args=["Resources/GOOG1/GOOGBook.csv", "GOOG"]),
        threading.Thread(target=transactionLoop, args=["Resources/INTC1/INTCBook.csv", "INTC"])
    ]
    for STOCK in STOCK_THREADS:
        STOCK.start()

    app.run(debug=True, threaded=True)
    THREADENABLED = False
    
    for STOCK in STOCK_THREADS:
        STOCK.join()
        
    exit(0)
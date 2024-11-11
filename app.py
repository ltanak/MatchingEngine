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
    with open(dataSource, newline = "") as csvfile: # Reading CSV
        file = csv.reader(csvfile, delimiter = ",", quotechar= "|")  
        for data in file:
            if not THREADENABLED: # If main thread terminates will break out of function
                break
            else:
                time.sleep(0.2)
                if accountType.isWaiting(): # Only processing one user order if there is one in the queue
                    userTransaction = accountType.popOrderQueue()
                    accountType.addLiveOrder(userTransaction)
                    matching(engine, userTransaction, stock)

                data = list(data)
                if data[1] == "1": # If data is valid execute
                    newTransaction = Transaction(fromCSV= data)
                    matching(engine, newTransaction, stock)
    return -1

"""
Performs matching functionson incoming transaction and assocaited engine
Adds volatility to the stock
If not matched, update with the previous traded value
Check if any transaction is a user one, if it is update associated user account
"""

def matching(engine: MatchingEngine, transaction: Transaction, stock):
    stockEngine = ENGINE_COLLECTION.getEngine(stock)

    transaction.price = int(transaction.price * (1 + random.uniform(-0.001, 0.001))) # Added volatility to make data more interesting

    engine.addToBook(transaction)
    matchedPair = engine.getMostRecentMatch()
    matched = engine.priceTimePriority()
    if not matched:
        for order in matchedPair:   # Check if previous is still a user transaction
            checkUser(engine, order, stock)

    while matched:
        newVolume = transaction.quantity if transaction.type == "BID" else -transaction.quantity
        stockEngine._updateAll(transaction.price, (time.time() - LOCALSTARTTIME) * 100, newVolume) # Update stock engine with new trade
        print(f"{stock}: {time.time() - LOCALSTARTTIME} , {transaction.price}") # Output to terminal trade matched

        matchedPair = engine.getMostRecentMatch() # Check if new trade is a user transaction
        for order in matchedPair:
            checkUser(engine, order, stock)

        matched = engine.priceTimePriority() # Check if trades can still be matched
    

    if stockEngine.getCurrentPrice() != None: # If transaction is valid, update engine for it to be plotted
        stockEngine._updateAll(stockEngine.getCurrentPrice(), (time.time() - LOCALSTARTTIME) * 100, stockEngine.getCurrentVolume())

"""
Check if a transaction is from a user, update values accordingly
If it is in user orders, but not in engine - trade fully matched
Otherwise, update specific transaction to new amounts
"""

def checkUser(engine: MatchingEngine, transaction: Transaction, stock: str):
    account = PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1: # If not present returns -1
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)

"""
Page API redirects and template rendering
"""

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

"""
API endpoint for plotting transaction on graph
Takes in stock type as input
Returns most recent timestamp and price, as an array for that stock
"""

@app.route('/matchingData', methods=["GET", "POST"])
def matchingData():
    stock = request.args.get('stockType')

    stockEngine = ENGINE_COLLECTION.getEngine(stock)
    data = [stockEngine.getMostRecentTimestamp(), stockEngine.getCurrentPrice()]
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response

"""
API endpoint for stock and user information
Takes in stock type as input
Returns stock most recent price
Returns user balance, most recent stock bought price, order volume and P/L
"""

@app.route('/tradingValue', methods=["GET", "POST"])
def tradingInformation():
    stock = request.args.get('stock')
    accountType = PORTFOLIO.getAccount(stock)
    stockEngine = ENGINE_COLLECTION.getEngine(stock)
    return jsonify( # Returns JSON object as dictionary
        price = stockEngine.getCurrentPrice(), 
        userPrice = accountType.accountBalance, 
        userValue = accountType.stockBoughtAt, 
        userStock = accountType.totalOrderVolume, 
        PL = accountType.currentPL)

"""
API endpoint for user placing order
POST request taking in the stock, volume and orderType
Turns input into transaction object, if input is valid places order
"""

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

"""
API endpoint for preloading graphs with previous data
Takes stock as input
Returns JSON containing all traded prices and corresponding timestamps
"""

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

    
if __name__ == '__main__':

    # Defining individual threads for each stock implementation

    STOCK_THREADS = [
        threading.Thread(target=transactionLoop, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"]),
        threading.Thread(target=transactionLoop, args=["Resources/AAPL1/AAPLBook.csv", "AAPL"]),
        threading.Thread(target=transactionLoop, args=["Resources/AMZN1/AMZNBook.csv", "AMZN"]),
        threading.Thread(target=transactionLoop, args=["Resources/GOOG1/GOOGBook.csv", "GOOG"]),
        threading.Thread(target=transactionLoop, args=["Resources/INTC1/INTCBook.csv", "INTC"])
    ]

    for STOCK in STOCK_THREADS: # Starting the execution of each thread
        STOCK.start()

    app.run(debug=True, threaded=True)

    THREADENABLED = False # When main thread quits flask app, threads stop executing function
    
    for STOCK in STOCK_THREADS: # Close all threads
        STOCK.join()
        
    exit(0)
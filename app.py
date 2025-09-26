from flask import Flask
from src.routes.routes import bp
import src.globals.globals as g
from src.classes.MatchingEngine import MatchingEngine
from src.classes.Transaction import Transaction
from src.classes.TradedEngine import TradedEngine
from src.classes.User import User
from src.classes.Portfolio import Portfolio
from src.classes.TradedEngineCollection import TradedEngineCollection
import threading, time, random, csv

app = Flask(__name__)
app.register_blueprint(bp)

LOCALSTARTTIME = time.time()
THREADENABLED = True

MSFT_ENGINE = TradedEngine()
AAPL_ENGINE = TradedEngine()
AMZN_ENGINE = TradedEngine()
GOOG_ENGINE = TradedEngine()
INTC_ENGINE = TradedEngine()

STOCK_ENGINES = {
    "MSFT": MSFT_ENGINE,
    "AAPL": AAPL_ENGINE,
    "AMZN": AMZN_ENGINE,
    "GOOG": GOOG_ENGINE,
    "INTC": INTC_ENGINE,
}

MSFT_ACCOUNT = User(accountBalance=1000000)
AMZN_ACCOUNT = User(accountBalance=10000000)
GOOG_ACCOUNT = User(accountBalance=10000000)
AAPL_ACCOUNT = User(accountBalance=10000000)
INTC_ACCOUNT = User(accountBalance=1000000)

STOCK_ACCOUNTS = {
    "MSFT": MSFT_ACCOUNT,
    "AAPL": AAPL_ACCOUNT,
    "AMZN": AMZN_ACCOUNT,
    "GOOG": GOOG_ACCOUNT,
    "INTC": INTC_ACCOUNT,
}

PORTFOLIO = Portfolio(STOCK_ACCOUNTS)
ENGINE_COLLECTION = TradedEngineCollection(STOCK_ENGINES)

# 🔑 assign into globals module
g.ENGINE_COLLECTION = ENGINE_COLLECTION
g.PORTFOLIO = PORTFOLIO
g.LOCALSTARTTIME = LOCALSTARTTIME

def transactionLoop(dataSource: str, stock: str) -> int:
    engine = MatchingEngine()
    accountType = PORTFOLIO.getAccount(stock)
    with open(dataSource, newline="") as csvfile:  # Reading CSV
        file = csv.reader(csvfile, delimiter=",", quotechar="|")
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
                if data[1] == "1":  # If data is valid execute
                    newTransaction = Transaction(fromCSV=data)
                    newTransaction.timestamp = time.time() - LOCALSTARTTIME
                    matching(engine, newTransaction, stock)
    return -1


def matching(engine: MatchingEngine, transaction: Transaction, stock) -> None:
    stockEngine = ENGINE_COLLECTION.getEngine(stock)

    transaction.price = int(
        transaction.price * (1 + random.uniform(-0.0005, 0.0005))
    )  # Add price variation

    engine.addToBook(transaction)
    matchedPair = engine.getMostRecentMatch()
    matched = engine.priceTimePriority()
    if not matched:
        for order in matchedPair:
            checkUser(engine, order, stock)

    while matched:
        newVolume = transaction.quantity if transaction.type == "BID" else -transaction.quantity
        stockEngine._updateAll(transaction.price, (time.time() - LOCALSTARTTIME) * 100, newVolume)

        matchedPair = engine.getMostRecentMatch()
        for order in matchedPair:
            checkUser(engine, order, stock)

        matched = engine.priceTimePriority()

    if stockEngine.getCurrentPrice() is not None:
        stockEngine._updateAll(
            stockEngine.getCurrentPrice(),
            (time.time() - LOCALSTARTTIME) * 100,
            stockEngine.getCurrentVolume(),
        )


def checkUser(engine: MatchingEngine, transaction: Transaction, stock: str) -> None:
    account = PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)


if __name__ == "__main__":
    STOCK_THREADS = [
        threading.Thread(target=transactionLoop, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"]),
        threading.Thread(target=transactionLoop, args=["Resources/AAPL1/AAPLBook.csv", "AAPL"]),
        threading.Thread(target=transactionLoop, args=["Resources/AMZN1/AMZNBook.csv", "AMZN"]),
        threading.Thread(target=transactionLoop, args=["Resources/GOOG1/GOOGBook.csv", "GOOG"]),
        threading.Thread(target=transactionLoop, args=["Resources/INTC1/INTCBook.csv", "INTC"]),
    ]

    for STOCK in STOCK_THREADS:
        STOCK.start()

    app.run(debug=True, threaded=True)

    THREADENABLED = False
    for STOCK in STOCK_THREADS:
        STOCK.join()

    exit(0)

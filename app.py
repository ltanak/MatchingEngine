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
from src.simulation import transactionLoop

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
g.THREADENABLED = THREADENABLED

if __name__ == "__main__":
    STOCK_THREADS = [
        threading.Thread(target=transactionLoop, args=["Resources/MSFT1/MSFTBook.csv", "MSFT"], kwargs={"delay": 0.2}),
        threading.Thread(target=transactionLoop, args=["Resources/AAPL1/AAPLBook.csv", "AAPL"], kwargs={"delay": 0.2}),
        threading.Thread(target=transactionLoop, args=["Resources/AMZN1/AMZNBook.csv", "AMZN"], kwargs={"delay": 0.2}),
        threading.Thread(target=transactionLoop, args=["Resources/GOOG1/GOOGBook.csv", "GOOG"], kwargs={"delay": 0.2}),
        threading.Thread(target=transactionLoop, args=["Resources/INTC1/INTCBook.csv", "INTC"], kwargs={"delay": 0.2}),
    ]

    for STOCK in STOCK_THREADS:
        STOCK.start()

    app.run(debug=True, threaded=True)

    THREADENABLED = False
    for STOCK in STOCK_THREADS:
        STOCK.join()

    exit(0)
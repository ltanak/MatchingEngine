import threading
import src.globals.globals as g
from src.simulation import transactionLoop
from src.classes.TradedEngine import TradedEngine
from src.classes.User import User
from src.classes.Portfolio import Portfolio
from src.classes.TradedEngineCollection import TradedEngineCollection
from benchmarking.benchlib import bench, run_benchmarks

def setup_environment():
    g.LOCALSTARTTIME = 0
    g.THREADENABLED = True

    # Stock engines
    stock_engines = {
        "MSFT": TradedEngine(),
        "AAPL": TradedEngine(),
        "AMZN": TradedEngine(),
        "GOOG": TradedEngine(),
        "INTC": TradedEngine(),
    }

    # Stock accounts
    stock_accounts = {
        "MSFT": User(accountBalance=1000000),
        "AAPL": User(accountBalance=1000000),
        "AMZN": User(accountBalance=1000000),
        "GOOG": User(accountBalance=1000000),
        "INTC": User(accountBalance=1000000),
    }

    g.PORTFOLIO = Portfolio(stock_accounts)
    g.ENGINE_COLLECTION = TradedEngineCollection(stock_engines)


def bench_single_stock(limit: int = None):
    """Benchmark transactionLoop on a single stock CSV."""
    setup_environment()
    transactionLoop("Resources/MSFT1/MSFTBook.csv", "MSFT", maxOrders= limit)


def bench_multi_thread(limit: int = None):
    """Benchmark running multiple stock loops in parallel threads."""
    setup_environment()
    stocks = [
        ("Resources/MSFT1/MSFTBook.csv", "MSFT"),
        ("Resources/AAPL1/AAPLBook.csv", "AAPL"),
        ("Resources/AMZN1/AMZNBook.csv", "AMZN"),
        ("Resources/GOOG1/GOOGBook.csv", "GOOG"),
        ("Resources/INTC1/INTCBook.csv", "INTC"),
    ]
    threads = [threading.Thread(target=transactionLoop, args=args, kwargs={"maxOrders": limit}) for args in stocks]

    for t in threads:
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    results = []
    results.append(bench(bench_single_stock, runs=3, limit=None))
    results.append(bench(bench_multi_thread, runs=3, limit=None))
    run_benchmarks(results)

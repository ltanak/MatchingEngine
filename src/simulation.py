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


def transactionLoop(dataSource: str, stock: str) -> int:
    engine = MatchingEngine()
    accountType = g.PORTFOLIO.getAccount(stock)
    with open(dataSource, newline="") as csvfile:  # Reading CSV
        file = csv.reader(csvfile, delimiter=",", quotechar="|")
        for data in file:
            if not g.THREADENABLED:
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
                    newTransaction.timestamp = time.time() - g.LOCALSTARTTIME
                    matching(engine, newTransaction, stock)
    return -1


def matching(engine: MatchingEngine, transaction: Transaction, stock) -> None:
    stockEngine = g.ENGINE_COLLECTION.getEngine(stock)

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
        stockEngine._updateAll(transaction.price, (time.time() - g.LOCALSTARTTIME) * 100, newVolume)

        matchedPair = engine.getMostRecentMatch()
        for order in matchedPair:
            checkUser(engine, order, stock)

        matched = engine.priceTimePriority()

    if stockEngine.getCurrentPrice() is not None:
        stockEngine._updateAll(
            stockEngine.getCurrentPrice(),
            (time.time() - g.LOCALSTARTTIME) * 100,
            stockEngine.getCurrentVolume(),
        )


def checkUser(engine: MatchingEngine, transaction: Transaction, stock: str) -> None:
    account = g.PORTFOLIO.getAccount(stock)
    if account.isUserOrder(transaction.id):
        if engine.getOrderFromId(transaction.id) == -1:
            account.removeLiveOrder(transaction.id)
        else:
            transaction = engine.getOrderFromId(transaction.id)
            account.updateValues(transaction)

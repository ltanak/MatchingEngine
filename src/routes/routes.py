from flask import Blueprint, request, redirect, render_template, jsonify, make_response
import json, time

from src.classes.Transaction import Transaction
import src.globals.globals as g

bp = Blueprint("routes", __name__)

@bp.route("/", methods=["GET", "POST"])
def main():
    return redirect("/msft.html")

@bp.route("/msft.html", methods=["GET", "POST"])
def msft():
    return render_template("msft.html")

@bp.route("/aapl.html", methods=["GET", "POST"])
def aapl():
    return render_template("aapl.html")

@bp.route("/amzn.html", methods=["GET", "POST"])
def amzn():
    return render_template("amzn.html")

@bp.route("/goog.html", methods=["GET", "POST"])
def goog():
    return render_template("goog.html")

@bp.route("/intc.html", methods=["GET", "POST"])
def intc():
    return render_template("intc.html")

@bp.route("/matchingData", methods=["GET", "POST"])
def matchingData():
    stock = request.args.get("stockType")
    stockEngine = g.ENGINE_COLLECTION.getEngine(stock)

    data = [stockEngine.getMostRecentTimestamp(), stockEngine.getCurrentPrice()]
    response = make_response(json.dumps(data))
    response.content_type = "application/json"
    return response

@bp.route("/tradingValue", methods=["GET", "POST"])
def tradingInformation():
    stock = request.args.get("stock")
    accountType = g.PORTFOLIO.getAccount(stock)
    stockEngine = g.ENGINE_COLLECTION.getEngine(stock)
    return jsonify(
        price=stockEngine.getCurrentPrice(),
        userPrice=accountType.accountBalance,
        userValue=accountType.stockBoughtAt,
        userStock=accountType.totalOrderVolume,
        PL=accountType.currentPL,
    )

@bp.route("/userPlaceOrder", methods=["POST"])
def userPlaceOrder():
    stock = request.form["stock"]
    stockEngine = g.ENGINE_COLLECTION.getEngine(stock)
    accountType = g.PORTFOLIO.getAccount(stock)

    volume = request.form["volume"]
    orderType = request.form["orderType"]
    userTransaction = Transaction()
    userTransaction.setTransaction(
        time.time() - g.LOCALSTARTTIME, orderType, stockEngine.getCurrentPrice(), float(volume)
    )
    accountType.placeOrder(userTransaction)
    return "Trade submitted"

@bp.route("/preloadData", methods=["GET", "POST"])
def preloadData():
    stock = request.args.get("stock")
    engine = g.ENGINE_COLLECTION.getEngine(stock)
    return jsonify(prices=engine.getAllPrices(), timestamps=engine.getAllTimestamps())

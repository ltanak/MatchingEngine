from TradedEngine import TradedEngine

class TradedEngineCollection:

    def __init__(self, stockEngines: list[TradedEngine]):
        self.engines = {
            "MSFT": stockEngines[0],
            "AAPL": stockEngines[1],
            "AMZN": stockEngines[2],
            "GOOG": stockEngines[3],
            "INTC": stockEngines[4]
        }

    def getEngine(self, stock):
        return self.engines[stock]
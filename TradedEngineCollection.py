from TradedEngine import TradedEngine

class TradedEngineCollection:

    def __init__(self, stockEngines: dict[str, TradedEngine]):
        self.engines = stockEngines

    def getEngine(self, stock):
        return self.engines[stock]
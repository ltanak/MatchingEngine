from TradedEngine import TradedEngine

"""
Class to store all corresponding trading engines
Returns specific engine on query
"""

class TradedEngineCollection:

    def __init__(self, stockEngines: dict[str, TradedEngine]):
        self.engines = stockEngines

    def getEngine(self, stock):
        return self.engines[stock]
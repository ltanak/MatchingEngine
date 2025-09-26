import time
import math

"""
Stores information on all matched trades
Used to return current pricing, all previous trades and timestamps
"""

class TradedEngine:

    def __init__(self):
        self._currentPrice = None
        self._mostRecentTimestamp = 0
        self._prices = []
        self._timestamps = []
        self._volume = 0
        self._ratio = 0

    # Get methods for attributes

    def getCurrentPrice(self):
        return self._currentPrice
    
    def getAllPrices(self):
        return self._prices
    
    def getAllTimestamps(self):
        return self._timestamps
    
    def getMostRecentTimestamp(self):
        return self._mostRecentTimestamp
    
    def getCurrentVolume(self):
        return self._volume
    
    # Setter methods for most attributes
    
    def _updatePrice(self, _newPrice):
        self._currentPrice = _newPrice

    def _updateTime(self, _newTime):
        self._mostRecentTimestamp = _newTime
    
    def _updateVolume(self, _newVolume):
        self._volume = _newVolume
    
    def getCurrentRatio(self, sizeBuy, sizeSell):
        return sizeBuy / sizeSell
    
    # Updates all relevant attributes at once

    def _updateAll(self, _newPrice, _newTimestamp, _newVolume):
        self._currentPrice = _newPrice
        self._mostRecentTimestamp = _newTimestamp
        self._volume = _newVolume
        self._prices.append(_newPrice)
        self._timestamps.append(_newTimestamp)
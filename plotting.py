import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

class Plotting:
    def __init__(self):
        self.minTime = float("inf")
        self.maxTime = -1
        self.minPrice = float("inf")
        self.maxPrice = -1
        self.arrayOfPrices = []
        self.arrayOfTimes = []

    def add(self, time, price):
        self.arrayOfPrices.append(price)
        self.arrayOfTimes.append(time)
        self.minPrice = min(self.minPrice, price)
        self.maxPrice = max(self.maxPrice, price)
        self.minTime = min(self.minTime, time)
        self.maxTime = max(self.maxTime, time)

    def plot(self):
        prices = np.array(self.arrayOfPrices)
        time = np.array(self.arrayOfTimes)
        plt.plot(time, prices)
        plt.show()
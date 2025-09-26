import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np
import matplotlib.animation as animation
from matplotlib import style

"""
Class for initial testing to visualise trade matching
"""

class Plotting:
    def __init__(self):
        self.arrayOfPrices = []
        self.arrayOfTimes = []

        self.fig = None
        self.ax1 = None

    def add(self, time, price): # Add input to arrays
        self.arrayOfPrices.append(price)
        self.arrayOfTimes.append(time)

    def plot(self): # Convert into numpy arrays for MPL to plot
        prices = np.array(self.arrayOfPrices)
        time = np.array(self.arrayOfTimes)
        plt.plot(time, prices)
        plt.show()

    def plotLive(self): # Attempt to dynamically plot on matplotlib
        style.use('fivethirtyeight')
        self.fig = plt.figure()
        self.ax1 = self.fig.add_subplot(1,1,1)
        ani = animation.FuncAnimation(self.fig, self.animate(), interval = 1000)
        plt.show()

    def animate(self):
        self.ax1.clear()
        self.ax1(np.array(self.arrayOfPrices), np.array(self.arrayOfTimes))
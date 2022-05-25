from command import Command
import csv
import json
import pprint
import time
from datetime import datetime

import ccxt
import matplotlib.pyplot as plt
import numpy
import pandas as pd
from mplfinance.original_flavor import candlestick_ohlc
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from algorithm_implementation.buy import Buy
from algorithm_implementation.sell import Sell
from telegram_implementation import Telegram


class HistoryManager(Command):

    def execute(self):
        pass

    def __init__(self, controller, config):
        super().__init__(controller)
        self.fetch_filename = config['fetchHistory']['filename']
        self.since = controller.since

    # method to fetch history into a file
    def fetch_history(self):
        # download
        print("downloading...")
        history = self.controller.fetch_ohlcv(since=self.since * 1000)
        last_timestamp = 1
        this_timestamp = 0
        while last_timestamp != this_timestamp:
            time.sleep(self.controller.exchange.rateLimit / 1000)
            print(history)
            last_timestamp = history[-1][0]
            history = history + self.controller.fetch_ohlcv(since=last_timestamp + 1)
            this_timestamp = history[-1][0]

        pprint.pprint(history)
        print("Length: " + str(len(history)))
        # save
        csv_file = open(self.fetch_filename, "w", newline="")
        writer = csv.writer(csv_file, delimiter=",")
        for candlestick in history:
            writer.writerow(candlestick)
        csv_file.close()
        print("finished")

    # method to visually show history from specific file
    def show_history(self):
        print("showing history...")
        df = pd.DataFrame(self.controller.loaded_history)
        for index in range(len(df)):
            df[0][index] = index
        plt.style.use('ggplot')
        fig, ax = plt.subplots()
        candlestick_ohlc(ax, df.values, width=0.5, colorup='blue', colordown='red')
        plt.show()
        return plt
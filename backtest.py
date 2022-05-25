from datetime import datetime
import matplotlib.pyplot as plt
from algorithm_implementation.buy import Buy
from algorithm_implementation.sell import Sell
from command import Command
from controller import Controller


class Backtest(Command):

    def __init__(self, controller):
        super().__init__(controller)
        self.loaded_history = self.controller.loaded_history
        self.fee = self.controller.fee
        self.symbol = self.controller.symbol
        self.module = self.controller.module
        self.algorithm = self.controller.algorithm
        self.exchange = self.controller.exchange

    # helper method to execute a single back test, returns all the parameters to create a graph
    def backtest_execution(self, fee, other_algorithm=None):
        history = self.loaded_history
        if other_algorithm is None:
            algorithm = self.algorithm
        else:
            algorithm = other_algorithm
        algorithm.controller = self.controller
        algorithm.init_algorithm(algorithm)
        base_currency = 1
        quote_currency = 0
        dates = []
        price = []
        buy_dates = []
        buy_price = []
        sell_dates = []
        sell_price = []
        for x in range(500, len(history)):
            date = datetime.fromtimestamp(history[x][0] / 1000)
            dates.append(date)
            side = algorithm.on_new_data(algorithm, history[x - 500:x])
            current_value = base_currency + quote_currency / history[x][4]
            if side == Controller.SELL:
                quote_currency += history[x][4] * base_currency * (1 - fee / 100)
                base_currency = 0
                sell_dates.append(date)
                sell_price.append(current_value)
            if side == Controller.BUY:
                base_currency += quote_currency / history[x][4] * (1 - fee / 100)
                quote_currency = 0
                buy_dates.append(date)
                buy_price.append(current_value)
            price.append(current_value)
        return (dates, price), (sell_dates, sell_price), (buy_dates, buy_price)

    # method that executes all important backtests with the algorithm and visualizes the result
    def backtest(self):
        print("backtesting...")
        # gather tests
        backtests = [self.backtest_execution(self.fee, Buy), self.backtest_execution(self.fee, Sell),
                     self.backtest_execution(0), self.backtest_execution(self.fee)]
        base = self.symbol.split("/")[0]
        quote = self.symbol.split("/")[1]
        info = ['buy and hold of ' + base, 'buy and hold of ' + quote, 'algorithm, without fees',
                'algorithm, with fees']
        # plot
        i = 0
        for backtest in backtests:
            print("You have {0}% of your initial portfolio after {1} trades ({2})".format(
                str(backtest[0][1][-1] * 100), str(len(backtest[1][0]) + len(backtest[2][0])), info[i]))
            plt.plot(backtest[0][0], backtest[0][1], label=info[i])
            if i == 3:
                plt.plot(backtest[1][0], backtest[1][1], 'ro', label='SELL ' + base + ' for ' + quote)
                plt.plot(backtest[2][0], backtest[2][1], 'go', label='BUY ' + base + ' for ' + quote)
            else:
                plt.plot(backtest[1][0], backtest[1][1], 'ro')
                plt.plot(backtest[2][0], backtest[2][1], 'go')
            i = i + 1
        plt.ylabel(base)
        plt.title("Backtest of " + self.module + " " + str(self.algorithm.get_standard_parameters(self.algorithm)))
        plt.gcf().autofmt_xdate()
        plt.legend(loc='upper left')
        plt.show()

    def execute(self):
        self.backtest()

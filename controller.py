import json
import ccxt
import numpy


class Controller:
    # static variables for buying and selling
    BUY = 'buy'
    SELL = 'sell'

    # load the config information into global variables
    def __init__(self):
        f = open('config.json')
        config = json.load(f)
        self.module = config['algorithmModule']
        self.classname = config['algorithmClassName']
        self.fee = config['fee']
        self.timeframe = config['timeframe']
        self.since = config['fetchHistory']['since']
        self.amount = config['run']['amount']
        self.symbol = config['tradingpair']
        self.exchange = getattr(ccxt, config['exchange'])({
            'apiKey': config['login']['apiKey'],
            'secret': config['login']['secret'],
            'enableRateLimit': True,
            'options': {'defaultType': 'spot'},
        })

        try:
            self.loaded_history = numpy.genfromtxt(config['history'], delimiter=',')
        except:
            print("No history available")

        mod = __import__('algorithm_implementation.' + self.module, fromlist=[self.classname])
        self.algorithm = getattr(mod, 'Algorithm')
        self.algorithm.controller = self

        from backtest import Backtest
        from history_manager import HistoryManager
        from optimization import Optimization
        from real_trading import RealTrading
        from telegram_connector import TelegramConnector

        self.telegram_connector = TelegramConnector(self, config)
        self.real_trading = RealTrading(self, self.telegram_connector, config)
        self.backtest = Backtest(self)
        self.optimization = Optimization(self)
        self.history_manager = HistoryManager(self, config)

    # helper function to fetch history
    def fetch_ohlcv(self, since=None):
        return self.exchange.fetch_ohlcv(
            self.symbol, self.timeframe, since=since
        )

    # method that starts the correct part of the program
    def execute_command(self, command):
        if command == "run":
            self.real_trading.execute()
        elif command == "fetchHistory":
            self.history_manager.fetch_history()
        elif command == "showHistory":
            self.history_manager.show_history()
        elif command == "backtest":
            self.backtest.execute()
        elif command == "optimize":
            self.optimization.execute()

import time
import numpy
from command import Command
from controller import Controller


class RealTrading(Command):

    def __init__(self, controller, telegram_connector, config):
        super().__init__(controller)
        self.telegram_connector = telegram_connector
        self.test = config['run']['test']

    # helper function to execute trade
    def execute_trade(self, side, telegram=None):
        typ = 'market'
        price = None
        params = {'test': self.test}
        c = self.controller
        order = c.exchange.create_order(c.symbol, typ, side, c.amount, price, params)
        print(order)
        if telegram is not None and telegram.messaging is not None:
            telegram.messaging.reply_text(order)
        # telegram
        return order

    # execute the bot in real time
    def run(self):
        print("starting bot...")
        telegram = self.telegram_connector.init_telegram()

        # init algorithm
        mod = __import__(
            'algorithm_implementation.' + self.controller.module,
            fromlist=[self.controller.classname]
        )
        algorithm = getattr(mod, 'Algorithm')
        algorithm.controller = self.controller
        algorithm.init_algorithm(algorithm)

        last_timestamp = 0
        while True:
            time.sleep(self.controller.exchange.rateLimit / 1000)
            history = self.controller.fetch_ohlcv()
            if history[len(history) - 1][0] != last_timestamp:
                # new timestamp = new data
                last_timestamp = history[len(history) - 1][0]
                side = algorithm.on_new_data(algorithm, numpy.array(history))
                if side is Controller.SELL or side is Controller.BUY:
                    self.execute_trade(side, telegram=telegram)

    def execute(self):
        self.run()

from base_algorithm import BaseAlgorithm
import talib


class Algorithm(BaseAlgorithm):
    OVERBOUGHT = 70
    OVERSOLD = 30
    PERIOD = 14
    last_operation = ""

    def get_possible_parameters(self):
        return [[60, 90], [10, 40], [3, 30]]

    def get_standard_parameters(self):
        return [self.OVERBOUGHT, self.OVERSOLD, self.PERIOD]

    def init_algorithm(self, parameter=None):
        self.last_operation = self.controller.BUY
        if parameter is not None:
            self.OVERBOUGHT = parameter[0]
            self.OVERSOLD = parameter[1]
            self.PERIOD = parameter[2]

    def on_new_data(self, new_history):
        rsi = talib.RSI(new_history[:, 4], self.PERIOD)
        value = rsi[len(rsi) - 1]

        if value > self.OVERBOUGHT and self.last_operation == self.controller.SELL:
            self.last_operation = self.controller.BUY
            return self.controller.BUY

        if value < self.OVERSOLD and self.last_operation == self.controller.BUY:
            self.last_operation = self.controller.SELL
            return self.controller.SELL
        return

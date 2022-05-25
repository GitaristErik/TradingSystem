from base_algorithm import BaseAlgorithm


class Sell(BaseAlgorithm):
    sold = False

    def get_possible_parameters(self):
        return []

    def get_standard_parameters(self):
        return []

    def init_algorithm(self, parameter=None):
        pass

    def on_new_data(self, new_history):
        if self.sold:
            return
        self.sold = True
        return self.controller.SELL

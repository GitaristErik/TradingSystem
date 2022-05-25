import numpy
from geneticalgorithm import geneticalgorithm as ga
from scipy.optimize import brute

from command import Command
from controller import Controller


class Optimization(Command):

    def __init__(self, controller) -> None:
        super().__init__(controller)
        self.loaded_history = controller.loaded_history

    def execute(self):
        self.optimize_genetic()
        self.optimize_brute_force()

    # more efficient backtesting function, that only tracks the profit
    # -> used for optimization -> return 1 / result because you want max instead of min
    def fitness(self, parameters):
        history = self.loaded_history
        algorithm = self.controller.algorithm
        fee = self.controller.fee

        algorithm.init_algorithm(algorithm, parameters)
        base_currency = 1
        quote_currency = 0
        for x in range(500, len(history)):
            side = algorithm.on_new_data(algorithm, history[x - 500:x])
            if side == Controller.SELL:
                quote_currency = quote_currency + history[x][4] * base_currency * (1 - fee / 100)
                base_currency = 0
            if side == Controller.BUY:
                base_currency = base_currency + quote_currency / history[x][4] * (1 - fee / 100)
                quote_currency = 0
        result = base_currency + quote_currency / history[-1][4]
        return 1 / result

    # method that optimizes the fitness function via genetic algorithm
    def optimize_genetic(self):
        print("optimizing via genetic alg...")
        algorithm_param = {
            'max_num_iteration': 100,
            'population_size': 10,
            'mutation_probability': 0.1,
            'elit_ratio': 0.01,
            'crossover_probability': 0.5,
            'parents_portion': 0.3,
            'crossover_type': 'uniform',
            'max_iteration_without_improv': 100
        }

        bounds = self.controller.algorithm.get_possible_parameters(self.controller.algorithm)
        model = ga(
            function=self.fitness,
            dimension=len(bounds),
            variable_type=type(bounds[0][0]).__name__,
            variable_boundaries=numpy.array(bounds),
            algorithm_parameters=algorithm_param
        )
        val = model.run()
        print(val)

    # method that optimizes the fitness function by trying all possibilities
    def optimize_brute_force(self):
        print("optimizing via scipy minimize optimization...")
        a = self.controller.algorithm
        bounds = numpy.array(a.get_possible_parameters(a))
        sol = brute(self.fitness, bounds)
        print(sol)

import warnings
from controller import Controller


def warn(*args, **kwargs):
    pass


# warnings.warn = warn

def parse_command_line():
    import argparse
    parser = argparse.ArgumentParser(description='Run the trading system')
    parser.add_argument(
        '--mode', type=str,
        choices=['backtest', 'run', 'optimize', 'fetchHistory', 'showHistory'],
        help='Mode to run the trading system'
    )
    # parser.add_argument('--backtest', type=str, default='backtest',
    #                     help='execute backtest of downloaded hystory')
    # parser.add_argument('--optimization', type=str, default='optimization',
    #                     help='run optimization of the algorithm')
    # parser.add_argument('--fetchHistory', type=str, default='fetchHistory',
    #                     help='download history from exchange')
    # parser.add_argument('--showHistory', type=str, default='showHistory',
    #                     help='visualize price line from file')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    command = parse_command_line()
    controller = Controller()
    controller.execute_command(command.mode)

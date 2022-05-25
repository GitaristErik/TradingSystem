from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from command import Command
from telegram_implementation import Telegram
import pprint


class TelegramConnector(Command):

    def __init__(self, controller, config):
        super().__init__(controller)
        self.telegram_enabled = config['run']['telegram']['enabled']
        self.telegram_token = config['run']['telegram']['token']
        # self.telegram_bot = self.init_telegram()

    # helper function to get information about holdings (telegram)
    def get_holdings(self):
        all_balances = self.controller.exchange.fetch_balance()['free']
        pprint.pprint(all_balances)
        return all_balances

    # method to initialize all the telegram features
    def init_telegram(self):
        if not self.telegram_enabled:
            return
        updater = Updater(self.telegram_token, use_context=True)
        dispatcher = updater.dispatcher
        telegram = Telegram(connector=self)
        dispatcher.add_handler(CommandHandler("start", telegram.start))
        dispatcher.add_handler(CommandHandler("stop", telegram.stop))
        dispatcher.add_handler(CommandHandler("help", telegram.help))
        dispatcher.add_handler(CommandHandler("status", telegram.status))
        dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, telegram.response))
        updater.start_polling()
        return telegram

    def execute(self):
        self.init_telegram()

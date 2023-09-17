from manager import BotManager
from config import TOKEN

#запуск бота
if __name__ == "__main__":
    bot_manager = BotManager(TOKEN)
    bot_manager.start()

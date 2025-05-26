from Config import Config
from Database import Database
from RedditHandler import RedditHandler
import RedditHandler

class AppContext:
    def __init__(self, config_path = 'config.ini'):
        self.config = Config(config_path)
        self.reddit = RedditHandler(self.config)
        self.db = Database(self.config.DATABASE_PATH)

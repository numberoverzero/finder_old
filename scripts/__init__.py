from mtg_search import app
from pymongo import MongoClient


class FlaskMongoMock(object):
    '''Doesn't requre current_app to load db'''
    def __init__(self, config):
        self.client = MongoClient(config['MONGO_URI'])

    @property
    def db(self):
        return self.client[config['MONGO_DB']]

config = app.config
mongo = FlaskMongoMock(config)

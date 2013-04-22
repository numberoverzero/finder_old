from flask.ext import restful, sqlalchemy
from flask import Flask

from util import fileutil


# Set root folder for loading files
fileutil.set_root(__file__)

app = Flask(__name__)
fileutil.load_config(app.config, '.config')
api = restful.Api(app)
db = sqlalchemy.SQLAlchemy(app)

import mtg_search.views

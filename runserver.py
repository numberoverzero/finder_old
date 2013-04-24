import logging
import sys

from mtg_search import app
app.run(debug=True)


handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

app.logger.addHandler(handler)

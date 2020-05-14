from flask import Flask
import highlight_text
import os
import requests
import operator
import re
import nltk

from werkzeug.exceptions import abort
from flask import Markup
#from flaskr.auth import login_required
#from flaskr.db import get_db


app = Flask(__name__)

app.register_blueprint(highlight_text.bp)
app.add_url_rule('/', endpoint='index')

if __name__ == "__main__":
	app.run(debug=True)
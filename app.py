from flask import Flask
from flask import render_template
import highlight_text

#from flaskr.auth import login_required
#from flaskr.db import get_db
from config import *

app = Flask(__name__)
app.config.from_object(TestingConfig())

@app.route('/')
def index():
    return render_template('/cbs/test.html')

app.register_blueprint(highlight_text.bp)
app.add_url_rule('/home', endpoint='home')

if __name__ == "__main__":
	app.run(debug=True)
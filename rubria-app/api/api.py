import time
from flask import Flask

app = Flask(__name__)

@app.route('/time')
def test_route():
    return {'time': time.time()}

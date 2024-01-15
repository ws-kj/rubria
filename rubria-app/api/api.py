import time
from flask import Flask
import sqlite3

app = Flask(__name__)
db = 'rubria.db'

@app.route('/time')
def test_route():
    return {'time': time.time()}


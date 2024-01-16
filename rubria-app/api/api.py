from typing import Union, Dict, Any
from flask import Flask, request, g, session 
from flask_bcrypt import Bcrypt
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"
dbpath = "rubria.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath)
    db.row_factory = sqlite3.Row
    return db

def query_db(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return rv

def squery_db(query, args=()):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    if rv is None:
        return rv
    return rv[0]

@app.route("/")
def index():

    return {}, 200

@app.route("/register", methods=["POST"])
def register_user():
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = query_db("select * from users where email = ?", [email])
    if user is not None:
        print("user exists")
        return {"error": "user already exists"}, 409

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
   
    res = query_db("insert into users (first_name, last_name, email, password) values (?, ?, ?, ?))",
             [first_name, last_name, email, hashed_password])
    if res is not None:
        return {"error": "error creating account"}, 409

    id = squery_db("select user_id from users where email = ?", [email])
    if id is None:
        return {"error": "error accessing account id"}, 409

    session["id"] = id
    session["email"] = email

    return {}, 200

@app.route("/login", methods=["POST"])
def login_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user = squery_db("select * from users where email = ?", [email])
    if user is None:
        return {"error": "user does not exist"}, 409

    if not bcrypt.check_password_hash(user["password"], password):
        return {"error": "invalid password"}, 409

    session["email"] = user["email"]
    session["id"] = user["id"]

    return {}, 200

@app.route("/logout", methods=["POST"])
def logout_user():
    session.clear()
    return {}, 200

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

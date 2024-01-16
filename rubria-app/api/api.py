from typing import Union, Dict, Any
from flask import Flask, request, g, session 
from flask_bcrypt import Bcrypt
from flask_cors import CORS, cross_origin
import sqlite3

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app, supports_credentials=True)
app.config["CORS_HEADERS"] = "Content-Type"
app.secret_key = "testing"
dbpath = "rubria.db"

def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(dbpath, isolation_level=None)
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
    if rv is None or len(rv) == 0:
        return None
    return rv[0]

@app.route("/")
def index():
    return {}, 200

@app.route("/me")
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return {"error": "unauthorized"}, 401

    user = squery_db("select * from users where user_id=?", [user_id])
    if not user:
        return {"error": "server error"}, 401

    payload = {
        "user_id": user["user_id"],
        "email": user["email"],
        "first_name": user["first_name"],
        "last_name": user["last_name"]
    }

    return {"user": payload}, 200

@app.route("/register", methods=["POST"])
@cross_origin()
def register_user():
    if not request.json:
        return {"error": "bad form"}, 401

    first_name = request.json.get("first_name")
    last_name = request.json.get("last_name")
    email = request.json.get("email")
    password = request.json.get("password")

    user = query_db("select * from users where email = ?", [email])
    if user:
        return {"error": "user already exists"}, 401

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
     
    res = squery_db("insert into users (first_name, last_name, email, password) values (?, ?, ?, ?)",
             [first_name, last_name, email, hashed_password])
    if res != None:
        return {"error": hashed_password}, 401

    id = squery_db("select user_id from users where email = ?", [email])
    if id is None:
        return {"error": "error accessing account id"}, 401

    session["id"] = id
    session["email"] = email

    return {}, 200

@app.route("/login", methods=["POST"])
def login_user():
    if not request.json:
        return {"error": "bad form"}, 401

    email = request.json.get("email")
    password = request.json.get("password")

    user = squery_db("select * from users where email = ?", [email])
    if user is None:
        return {"error": "user does not exist"}, 401

    if not bcrypt.check_password_hash(user["password"], password):
        return {"error": "invalid password"}, 401

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

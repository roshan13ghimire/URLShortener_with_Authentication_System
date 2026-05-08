from flask import Flask,request,jsonify
from db import init_db
from db import get_db_connection
import random
import string

app = Flask(__name__)

init_db()

@app.route("/")
def home():
    return {"message": "backend is running "}

@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    name = data.get("name")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, password) VALUES (%s, %s)",
        (name, password)
    )

    conn.commit()
    conn.close()

    return jsonify({"message": "User created"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    name = data.get("name")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE name = %s AND password = %s",
        (name, password)
    )

    user = cursor.fetchone()
    conn.commit()
    conn.close()

    if user:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

def generate_short_code():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


@app.route("/shorten", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("long_url")

    short_code  = generate_short_code()
    short_url = f"http://127.0.0.1:5000//{short_code}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO shorturl (long_url, short_code, short_url) VALUES (%s, %s, %s)",
        (long_url, short_code, short_url)
    )

    conn.commit()
    conn.close()

    return jsonify({"short_code": short_code, "short_url": short_url}), 200

@app.route("/my-urls/<int:userid>", methods=["GET"])
def get_user_urls(userid):

    conn = get_db_connection()
    cursor = conn.cursor()


    cursor.execute(
        "SELECT * FROM shorturl WHERE userid = %s",
        (userid,)
    )

    user_urls = cursor.fetchall()

    conn.close()

    return jsonify(user_urls), 200



if __name__ == "__main__":
    app.run(debug=True)
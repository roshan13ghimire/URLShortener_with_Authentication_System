from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from db import init_db, get_db_connection

import random
import string

app = Flask(__name__)

CORS(app)

# initialize database
init_db()


# -------------------------
# HOME ROUTE
# -------------------------
@app.route("/")
def home():
    return {"message": "Backend is running"}


# -------------------------
# SIGNUP
# -------------------------
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

    return jsonify({
        "message": "User created successfully"
    }), 201


# -------------------------
# LOGIN
# -------------------------
@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    name = data.get("name")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE name=%s AND password=%s",
        (name, password)
    )

    user = cursor.fetchone()

    conn.close()

    if user:
        return jsonify({
            "message": "Login successful"
        }), 200

    else:
        return jsonify({
            "message": "Invalid credentials"
        }), 401


# -------------------------
# GENERATE SHORT CODE
# -------------------------
def generate_short_code():
    return ''.join(
        random.choices(
            string.ascii_letters + string.digits,
            k=6
        )
    )


# -------------------------
# SHORTEN URL
# -------------------------
@app.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    long_url = data.get("long_url")

    short_code = generate_short_code()

    short_url = f"http://127.0.0.1:5000/{short_code}"

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO shorturl
        (long_url, short_code, short_url)
        VALUES (%s, %s, %s)
        """,
        (long_url, short_code, short_url)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "short_code": short_code,
        "short_url": short_url
    }), 200


# -------------------------
# GET ALL URLS
# -------------------------
@app.route("/my-urls", methods=["GET"])
def get_user_urls():

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM shorturl"
    )

    urls = cursor.fetchall()

    conn.close()

    return jsonify(urls), 200


# -------------------------
# REDIRECT SHORT URL
# -------------------------
@app.route("/<short_code>")
def redirect_url(short_code):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM shorturl WHERE short_code=%s",
        (short_code,)
    )

    url = cursor.fetchone()

    conn.close()

    if url:
        return redirect(url["long_url"])

    else:
        return jsonify({
            "message": "URL not found"
        }), 404


# -------------------------
# RUN SERVER
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)
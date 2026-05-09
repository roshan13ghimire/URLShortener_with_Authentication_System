from flask import Blueprint, request, jsonify
from db import get_db_connection
import bcrypt

auth_bp = Blueprint("auth", __name__)


# -------------------------
# SIGNUP
# -------------------------
@auth_bp.route("/signup", methods=["POST"])
def signup():

    data = request.get_json()

    name = data.get("name")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    )

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO users (name, password) VALUES (%s, %s)",
        (name, hashed_password)
    )

    conn.commit()

    conn.close()

    return jsonify({
        "message": "User created successfully"
    }), 201


# -------------------------
# LOGIN
# -------------------------
@auth_bp.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    name = data.get("name")
    password = data.get("password")

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM users WHERE name=%s",
        (name,)
    )

    user = cursor.fetchone()

    conn.close()

    if user:

        password_match = bcrypt.checkpw(
            password.encode("utf-8"),
            user["password"].encode("utf-8")
        )

        if password_match:

            return jsonify({
                "message": "Login successful",
                "userid": user["userid"]
            }), 200

    return jsonify({
        "message": "Invalid credentials"
    }), 401
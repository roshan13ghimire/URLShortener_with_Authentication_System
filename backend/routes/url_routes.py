from flask import Blueprint, request, jsonify, redirect

from db import get_db_connection

from utils.helpers import generate_short_code


url_bp = Blueprint("url", __name__)


# -------------------------
# SHORTEN URL
# -------------------------
@url_bp.route("/shorten", methods=["POST"])
def shorten_url():

    data = request.get_json()

    long_url = data.get("long_url")

    user_id = data.get("user_id")

    short_code = generate_short_code()

    short_url = f"http://127.0.0.1:5000/{short_code}"

    conn = get_db_connection()

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO shorturl
        (user_id, long_url, short_code, short_url)
        VALUES (%s, %s, %s, %s)
        """,
        (
            user_id,
            long_url,
            short_code,
            short_url
        )
    )

    conn.commit()

    conn.close()

    return jsonify({
        "short_url": short_url,
        "short_code": short_code
    }), 200


# -------------------------
# GET USER URLS
# -------------------------
@url_bp.route("/my-urls/<int:userid>", methods=["GET"])
def get_user_urls(userid):

    conn = get_db_connection()

    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM shorturl WHERE user_id = %s",
        (userid,)
    )

    urls = cursor.fetchall()

    conn.close()

    return jsonify(urls), 200


# -------------------------
# REDIRECT URL
# -------------------------
@url_bp.route("/<short_code>")
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

    return jsonify({
        "message": "URL not found"
    }), 404
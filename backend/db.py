import mysql.connector

DB_NAME = "url_shortener_db"


def get_server_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password=""
    )


def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database=DB_NAME
    )


def init_db():
    conn = get_server_connection()
    cursor = conn.cursor()

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
    conn.close()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            userid INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL
        )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS shorturl (

        id INT AUTO_INCREMENT PRIMARY KEY,

        user_id INT,

        long_url VARCHAR(255) NOT NULL,
        short_code VARCHAR(10) NOT NULL,
        short_url VARCHAR(255) NOT NULL,

        FOREIGN KEY (user_id)
        REFERENCES users(userid)
        ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close() 
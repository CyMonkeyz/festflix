import sqlite3
import datetime
import config

def get_db_connection():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # biar hasil query bisa diakses dengan nama kolom
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_expired TIMESTAMP
        );
    ''')
    conn.commit()
    conn.close()

def create_user(username, email, password_hash):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash)
        )
        conn.commit()
        user_id = cursor.lastrowid
        conn.close()
        return user_id  # sukses, return ID user
    except sqlite3.IntegrityError:
        return None  # email/username sudah terdaftar

def get_user_by_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_user_by_email(email):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()
    return user

from werkzeug.security import check_password_hash

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

# Inisialisasi database saat pertama dijalankan
init_db()

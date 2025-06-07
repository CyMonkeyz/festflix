import sqlite3
import datetime
import config
from werkzeug.security import check_password_hash, generate_password_hash

def get_db_connection():
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # hasil query bisa diakses pakai nama kolom
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabel users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            subscription_expired TIMESTAMP
        );
    ''')

    # Tabel films
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS films (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            sinopsis TEXT,
            tahun INTEGER,
            path_poster TEXT,
            path_video TEXT NOT NULL,
            produser TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            rating_avg REAL DEFAULT 0,
            jumlah_review INTEGER DEFAULT 0
        );
    ''')


    # Tabel watch_history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS watch_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            film_id INTEGER NOT NULL,
            watched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(film_id) REFERENCES films(id)
        );
    ''')

    # Tabel subscription_history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscription_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            package TEXT NOT NULL,
            start_date TIMESTAMP NOT NULL,
            end_date TIMESTAMP NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        );
    ''')

    conn.commit()
    
# ===================== ADMIN =========================
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if not cursor.fetchone():
        cursor.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
            ('admin', 'admin@festflix.local', generate_password_hash('admin'))
        )
        conn.commit()
    conn.close()

# ===================== USER =========================
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
        return user_id
    except sqlite3.IntegrityError:
        return None

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

def verify_user(email, password):
    user = get_user_by_email(email)
    if user and check_password_hash(user['password_hash'], password):
        return user
    return None

# ===================== FILM =========================
def create_film(title, genre, sinopsis, tahun, path_poster, path_video, produser=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO films (title, genre, sinopsis, tahun, path_poster, path_video, produser) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (title, genre, sinopsis, tahun, path_poster, path_video, produser)
    )
    conn.commit()
    conn.close()
    
def update_film(film_id, title, genre, sinopsis, tahun, path_poster, path_video, produser):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        UPDATE films
        SET title=?, genre=?, sinopsis=?, tahun=?, path_poster=?, path_video=?, produser=?
        WHERE id=?
        """,
        (title, genre, sinopsis, tahun, path_poster, path_video, produser, film_id),
    )
    conn.commit()
    conn.close()

def get_all_films():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films")
    films = cursor.fetchall()
    conn.close()
    return films

def get_film_by_id(film_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM films WHERE id = ?", (film_id,))
    film = cursor.fetchone()
    conn.close()
    return film

# ===================== WATCH HISTORY =========================
def add_watch_history(user_id, film_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO watch_history (user_id, film_id) VALUES (?, ?)", (user_id, film_id))
    conn.commit()
    conn.close()

def count_watch_today(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT COUNT(*) FROM watch_history
        WHERE user_id = ? AND DATE(watched_at) = DATE('now','localtime')
    """, (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

def get_watch_history(user_id, limit=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if limit:
        cursor.execute("""
            SELECT * FROM watch_history
            WHERE user_id = ? ORDER BY watched_at DESC LIMIT ?
        """, (user_id, limit))
    else:
        cursor.execute("""
            SELECT * FROM watch_history
            WHERE user_id = ? ORDER BY watched_at DESC
        """, (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

# ===================== SUBSCRIPTION HISTORY =========================
def create_subscription_history(user_id, package, start_date, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO subscription_history (user_id, package, start_date, end_date) VALUES (?, ?, ?, ?)",
        (user_id, package, start_date, end_date)
    )
    conn.commit()
    conn.close()

def update_user_subscription(user_id, end_date):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET subscription_expired = ? WHERE id = ?",
        (end_date, user_id)
    )
    conn.commit()
    conn.close()

def get_subscription_info(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT subscription_expired FROM users WHERE id = ?", (user_id,)
    )
    row = cursor.fetchone()
    conn.close()
    return row['subscription_expired'] if row else None

# ============= INIT DB SAAT DIJALANKAN LANGSUNG ================
init_db()

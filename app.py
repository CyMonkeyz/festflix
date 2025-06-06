# app.py
# Entry point untuk menjalankan Flask application

import models
import config
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = config.SECRET_KEY

models.init_db()

# ===== Dekorator proteksi login =====
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ===== ROUTE REGISTER =====
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        # Validasi input
        if not all([username, email, password, confirm_password]):
            flash("Semua field harus diisi.", "danger")
        elif "@gmail.com" not in email:
            flash("Email harus pakai @gmail.com.", "danger")
        elif password != confirm_password:
            flash("Password dan konfirmasi password tidak sama.", "danger")
        elif models.get_user_by_email(email):
            flash("Email sudah terdaftar.", "danger")
        else:
            hash_pw = generate_password_hash(password)
            user_id = models.create_user(username, email, hash_pw)
            if user_id:
                flash("Registrasi sukses, silakan login!", "success")
                return redirect(url_for('login'))
            else:
                flash("Username/email sudah terdaftar.", "danger")
    return render_template('register.html')

# ===== ROUTE LOGIN =====
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = models.get_user_by_email(email)
        if not user:
            flash("Email belum terdaftar.", "danger")
        elif not check_password_hash(user['password_hash'], password):
            flash("Password salah.", "danger")
        else:
            session['user_id'] = user['id']
            flash("Login sukses, selamat datang!", "success")
            return redirect(url_for('dashboard'))
    return render_template('login.html')

# ===== ROUTE DASHBOARD (protected & dinamis) =====
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = models.get_user_by_id(user_id)
    films = models.get_all_films()
    exp_date = models.get_subscription_info(user_id)
    watch_today = models.count_watch_today(user_id)
    now_datetime = datetime.utcnow()  # Bisa pakai now() kalau mau pakai waktu lokal

    return render_template(
        'dashboard.html',
        user=user,
        films=films,
        subscription_expired=exp_date,
        watch_count_today=watch_today,
        now_datetime=now_datetime
    )

# ===== ROUTE LOGOUT =====
@app.route('/logout')
def logout():
    session.clear()
    flash("Berhasil logout.", "info")
    return redirect(url_for('login'))

# ===== ROUTE FILM DETAIL (stub, opsional bisa ditambah) =====
@app.route('/film/<int:film_id>')
@login_required
def film_detail(film_id):
    film = models.get_film_by_id(film_id)
    if not film:
        flash('Film tidak ditemukan', 'danger')
        return redirect(url_for('dashboard'))
    user_id = session['user_id']
    exp_date = models.get_subscription_info(user_id)
    now = datetime.utcnow()
    watch_today = models.count_watch_today(user_id)
    can_watch = False
    if exp_date and exp_date > now:
        can_watch = True
    elif watch_today < 2:
        can_watch = True
    user = models.get_user_by_id(user_id)
    return render_template(
        'film_detail.html',
        film=film,
        can_watch=can_watch,
        user=user
    )

if __name__ == '__main__':
    app.run(debug=True)

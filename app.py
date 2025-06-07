import models
import config
import os
from flask import Flask, render_template, redirect, url_for, request, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = config.SECRET_KEY

models.init_db()

# ====== GENRE LIST (Satu sumber, dipakai dashboard & admin) ======
GENRE_LIST = ["Action", "Drama", "Komedi", "Horror", "Sci-Fi"]

# ====== Upload config ======
UPLOAD_FOLDER_POSTER = os.path.join('static', 'posters')
UPLOAD_FOLDER_VIDEO = os.path.join('static', 'videos')
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}

os.makedirs(UPLOAD_FOLDER_POSTER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_VIDEO, exist_ok=True)

def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set

# ====== Dekorator proteksi login ======
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            flash('Anda tidak punya hak akses admin.', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# ====== Context processor biar session bisa dipakai di template ======
@app.context_processor
def inject_session():
    return dict(session=session)

# ====== ROUTE REGISTER ======
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
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

# ====== ROUTE LOGIN ======
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
            if user['username'] == 'admin' and password == 'admin':
                session['is_admin'] = True
                flash("Login admin sukses!", "success")
                return redirect(url_for('admin_panel'))
            else:
                session['is_admin'] = False
                flash("Login sukses, selamat datang!", "success")
                return redirect(url_for('dashboard'))
    return render_template('login.html')

# ====== ADMIN PANEL & CRUD FILM ======
@app.route('/admin')
@admin_required
def admin_panel():
    search_query = request.args.get('q', '').strip()
    films = models.get_all_films()
    if search_query:
        search_lower = search_query.lower()
        # Filter film by id (as string) or title
        films = [
            f for f in films
            if search_lower in str(f['id']).lower() or search_lower in f['title'].lower()
        ]
    return render_template('admin_panel.html', films=films, search_query=search_query)

@app.route('/admin/add_film', methods=['GET', 'POST'])
@admin_required
def add_film():
    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        sinopsis = request.form.get('sinopsis', '').strip()
        tahun = request.form.get('tahun')
        produser = request.form.get('produser')
        poster_file = request.files.get('poster')
        video_file = request.files.get('video')
        path_poster = ''
        path_video = ''

        # Validasi tahun harus int
        try:
            tahun_int = int(tahun)
        except (ValueError, TypeError):
            flash('Tahun harus berupa angka.', 'danger')
            return render_template('add_film.html', genre_list=GENRE_LIST)

        # Validasi sinopsis maksimal 500 kata
        if len(sinopsis.split()) > 500:
            flash('Sinopsis maksimal 500 kata.', 'danger')
            return render_template('add_film.html', genre_list=GENRE_LIST)

        # Upload poster
        if poster_file and allowed_file(poster_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            poster_filename = f"{title}_{poster_file.filename}"
            poster_path = os.path.join(UPLOAD_FOLDER_POSTER, poster_filename)
            poster_file.save(poster_path)
            path_poster = f'posters/{poster_filename}'
        # Upload video
        if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
            video_filename = f"{title}_{video_file.filename}"
            video_path = os.path.join(UPLOAD_FOLDER_VIDEO, video_filename)
            video_file.save(video_path)
            path_video = f'videos/{video_filename}'

        if not path_video:
            flash('File video wajib diupload dan harus berformat mp4/avi/mov!', 'danger')
            return render_template('add_film.html', genre_list=GENRE_LIST)

        models.create_film(title, genre, sinopsis, tahun_int, path_poster, path_video, produser)
        flash("Film berhasil ditambahkan!", "success")
        return redirect(url_for('admin_panel'))

    return render_template('add_film.html', genre_list=GENRE_LIST)

@app.route('/admin/edit_film/<int:film_id>', methods=['GET', 'POST'])
@admin_required
def edit_film(film_id):
    film = models.get_film_by_id(film_id)
    if not film:
        flash('Film tidak ditemukan!', 'danger')
        return redirect(url_for('admin_panel'))

    if request.method == 'POST':
        title = request.form.get('title')
        genre = request.form.get('genre')
        sinopsis = request.form.get('sinopsis', '').strip()
        tahun = request.form.get('tahun')
        produser = request.form.get('produser')
        poster_file = request.files.get('poster')
        video_file = request.files.get('video')
        path_poster = film['path_poster']
        path_video = film['path_video']

        # Validasi tahun harus int
        try:
            tahun_int = int(tahun)
        except (ValueError, TypeError):
            flash('Tahun harus berupa angka.', 'danger')
            return render_template('edit_film.html', film=film, genre_list=GENRE_LIST)

        if len(sinopsis.split()) > 500:
            flash('Sinopsis maksimal 500 kata.', 'danger')
            return render_template('edit_film.html', film=film, genre_list=GENRE_LIST)

        # Poster baru (opsional)
        if poster_file and allowed_file(poster_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            poster_filename = f"{title}_{poster_file.filename}"
            poster_path = os.path.join(UPLOAD_FOLDER_POSTER, poster_filename)
            poster_file.save(poster_path)
            path_poster = f'posters/{poster_filename}'
        # Video baru (opsional)
        if video_file and allowed_file(video_file.filename, ALLOWED_VIDEO_EXTENSIONS):
            video_filename = f"{title}_{video_file.filename}"
            video_path = os.path.join(UPLOAD_FOLDER_VIDEO, video_filename)
            video_file.save(video_path)
            path_video = f'videos/{video_filename}'

        # Update di DB (tambahkan fungsi baru di models.py: update_film)
        models.update_film(
            film_id, title, genre, sinopsis, tahun_int, path_poster, path_video, produser
        )
        flash("Data film berhasil diupdate!", "success")
        return redirect(url_for('admin_panel'))

    return render_template('edit_film.html', film=film, genre_list=GENRE_LIST)

@app.route('/admin/delete_film/<int:film_id>', methods=['POST'])
@admin_required
def delete_film(film_id):
    conn = models.get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM films WHERE id = ?", (film_id,))
    conn.commit()
    conn.close()
    flash("Film berhasil dihapus!", "info")
    return redirect(url_for('admin_panel'))

# ====== ROUTE DASHBOARD (protected & dinamis) ======
@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user = models.get_user_by_id(user_id)
    films = models.get_all_films()
    exp_date = models.get_subscription_info(user_id)
    watch_today = models.count_watch_today(user_id)
    now_datetime = datetime.utcnow()
    return render_template(
        'dashboard.html',
        user=user,
        films=films,
        genre_list=GENRE_LIST,
        subscription_expired=exp_date,
        watch_count_today=watch_today,
        now_datetime=now_datetime
    )

@app.route('/logout')
def logout():
    session.clear()
    flash("Berhasil logout.", "info")
    return redirect(url_for('login'))

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

# ====== ROUTE SUBSCRIBE ======
@app.route('/subscribe', methods=['GET', 'POST'])
@login_required
def subscribe():
    user_id = session['user_id']
    if request.method == 'POST':
        paket = request.form.get('package')  # '30_detik', '5_menit', '1_hari'
        now = datetime.utcnow()
        if not paket:
            flash('Pilih paket terlebih dahulu.', 'danger')
            return redirect(url_for('subscribe'))
        if paket == '30_detik':
            end = now + timedelta(seconds=30)
        elif paket == '5_menit':
            end = now + timedelta(minutes=5)
        elif paket == '1_hari':
            end = now + timedelta(days=1)
        else:
            flash('Pilihan paket tidak valid.', 'danger')
            return redirect(url_for('subscribe'))
        # Simpan ke subscription_history
        models.create_subscription_history(user_id, paket, now, end)
        # Update expired di users
        models.update_user_subscription(user_id, end)
        flash(f'Berhasil berlangganan sampai {end.strftime("%Y-%m-%d %H:%M")}', 'success')
        return redirect(url_for('dashboard'))
    return render_template('subscribe.html')


if __name__ == '__main__':
    app.run(debug=True)

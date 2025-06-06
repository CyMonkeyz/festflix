# app.py
# Entry point untuk menjalankan Flask application

# 1. Import Flask & config
from flask import Flask, render_template
import config

# 2. Buat objek app & set SECRET_KEY
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# 3. Buat route /
@app.route('/')
def dashboard():
    # Render dashboard.html
    return render_template('dashboard.html')

# 4. Jalankan app saat file ini dieksekusi langsung
if __name__ == '__main__':
    app.run(debug=True)

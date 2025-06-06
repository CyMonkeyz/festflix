# app.py
# Entry point untuk menjalankan Flask application

from flask import Flask, render_template, redirect, url_for
import config

app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY

# Buat satu function dashboard untuk dua route: '/' dan '/dashboard'
@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)

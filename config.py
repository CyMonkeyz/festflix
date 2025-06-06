import os
import secrets

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'festflix.db')
SECRET_KEY = '8140c80f130b7183ff78a8c47e29ec45'

print(secrets.token_hex(16)) #cuman buat generate code key

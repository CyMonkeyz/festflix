import os
import secrets; secrets.token_hex(16)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'festflix.db')
SECRET_KEY = 'ubah-ke-random-secret-key-nanti'

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app


def test_allowed_file_valid_image():
    assert app.allowed_file("poster.jpg", app.ALLOWED_IMAGE_EXTENSIONS)

def test_allowed_file_invalid_image():
    assert not app.allowed_file("poster.txt", app.ALLOWED_IMAGE_EXTENSIONS)

def test_allowed_file_valid_video():
    assert app.allowed_file("movie.mp4", app.ALLOWED_VIDEO_EXTENSIONS)

def test_allowed_file_invalid_video():
    assert not app.allowed_file("movie.exe", app.ALLOWED_VIDEO_EXTENSIONS)

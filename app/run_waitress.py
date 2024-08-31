# run_waitress.py
from waitress import serve
from app import app
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, current_dir)
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
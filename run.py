import subprocess
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PYTHON_DIR = os.path.join(BASE_DIR, "python")

subprocess.run(["python", "loginMenu.py"], cwd=PYTHON_DIR)
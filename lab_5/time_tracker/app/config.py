import os
from pathlib import Path

# Определяем пути
BASE_DIR = Path(__file__).resolve().parent.parent
DB_NAME = "tracker.db"
DB_PATH = os.path.join(BASE_DIR, DB_NAME)

# Настройки UI
APP_TITLE = "Хронометраж PRO"
APP_SIZE = "600x500"
THEME = "blue"  # blue, green, dark-blue
APPEARANCE_MODE = "Dark"  # System, Dark, Light
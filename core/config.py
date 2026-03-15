"""
Конфигурационный файл для приложения
"""

# Настройки приложения
APP_NAME = "日本語学習アプリ"
APP_VERSION = "1.0.0"
APP_WIDTH = 1300
APP_HEIGHT = 800

# Настройки базы данных
DB_NAME = "japanese_learning.db"

# Настройки путей
DATA_FILE = "japanese_data.json"
LOG_FILE = "app.log"

# Настройки цветов
COLORS = {
    "bg": "#f0f0f0",
    "fg": "#333333",
    "accent": "#4CAF50",
    "warning": "#ff9800",
    "error": "#f44336",
    "info": "#2196F3"
}

# Настройки шрифтов
FONTS = {
    "japanese": ("MS Mincho", 14),
    "default": ("Arial", 11),
    "title": ("Arial", 16, "bold"),
    "subtitle": ("Arial", 14, "bold")
}

# Уровни сложности
LEVELS = ["N5", "N4", "N3", "N2", "N1"]

# Главы книги
CHAPTERS = {
    "prologue": "プロローグ",
    "chapter1": "第一話『恋人』",
    "chapter2": "第二話『夫婦』",
    "chapter3": "第三話『姉妹』",
    "chapter4": "第四話『親子』"
}

# Типы упражнений
EXERCISE_TYPES = {
    "grammar": "文法",
    "vocab": "語彙",
    "kanji": "漢字",
    "comprehension": "読解"
}

# Интервалы для системы повторения (в днях)
REVIEW_INTERVALS = [1, 3, 7, 14, 30, 90, 180]
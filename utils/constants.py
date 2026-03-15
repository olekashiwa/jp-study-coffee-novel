"""
Константы приложения.
"""
# Пути
PATHS = {
    'DATA_DIR': 'data',
    'DB_FILE': 'japanese_learning.db',
    'LOG_FILE': 'app.log',
    'ASSETS_DIR': 'assets'
}

# Типы упражнений
EXERCISE_TYPES = {
    'grammar': {
        'name': '文法',
        'icon': '🔤',
        'color': '#2196F3'
    },
    'vocab': {
        'name': '語彙',
        'icon': '📚',
        'color': '#4CAF50'
    },
    'kanji': {
        'name': '漢字',
        'icon': '🈳',
        'color': '#FF9800'
    },
    'comprehension': {
        'name': '読解',
        'icon': '📖',
        'color': '#9C27B0'
    }
}

# Уровни JLPT
JLPT_LEVELS = ['N5', 'N4', 'N3', 'N2', 'N1']

# Цвета для уровней
LEVEL_COLORS = {
    'N5': '#4CAF50',
    'N4': '#8BC34A',
    'N3': '#FFC107',
    'N2': '#FF9800',
    'N1': '#F44336'
}

# Интервалы для SM-2 алгоритма
SM2_INTERVALS = [1, 6, 16, 45, 120, 300]

# Сообщения
MESSAGES = {
    'welcome': 'ようこそ！',
    'login_required': 'ログインしてください。',
    'success': '成功しました！',
    'error': 'エラーが発生しました。',
    'no_cards': '今日のカードはありません。'
}
"""
Управление базой данных SQLite. Все операции с БД.
"""
class Database:
    def __init__(self, db_path="japanese_learning.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        
    def create_tables(self):
        """Создание всех таблиц"""
        # users, progress, flashcards, etc.
        
    def execute_query(self, query, params=None):
        """Выполнение SQL-запроса"""
        
    def get_user(self, username):
        """Получение пользователя по имени"""
        
    def save_progress(self, user_id, chapter, exercise_type, score):
        """Сохранение прогресса"""
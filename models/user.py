"""
Модель пользователя.
"""
class User:
    def __init__(self, id, username, level, created_at):
        self.id = id
        self.username = username
        self.level = level  # N3, N2, N1
        self.created_at = created_at
        self.total_score = 0
        self.completed_exercises = []
        
    def update_score(self, points):
        """Обновление счета"""
        
    def get_progress(self):
        """Получение прогресса"""
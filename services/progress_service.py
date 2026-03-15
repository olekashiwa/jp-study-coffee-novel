"""
Сервис для отслеживания прогресса.
"""
class ProgressService:
    def __init__(self, database):
        self.db = database
        
    def record_exercise_result(self, user_id, exercise_id, correct):
        """Запись результата упражнения"""
        self.db.save_progress(user_id, exercise_id, correct)
        
    def get_user_progress(self, user_id):
        """Получение прогресса пользователя"""
        stats = {
            'total_exercises': self.db.count_completed_exercises(user_id),
            'correct_rate': self.db.get_correct_rate(user_id),
            'completed_chapters': self.db.get_completed_chapters(user_id),
            'weak_points': self.db.get_weak_points(user_id),
            'streak': self.db.get_current_streak(user_id)
        }
        return stats
    
    def get_learning_curve(self, user_id, days=30):
        """Получение кривой обучения за период"""
        data = self.db.get_daily_stats(user_id, days)
        return {
            'dates': [d['date'] for d in data],
            'scores': [d['score'] for d in data],
            'exercises': [d['count'] for d in data]
        }
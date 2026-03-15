"""
Сервис для генерации упражнений.
"""
class ExerciseService:
    def __init__(self, data_loader, database):
        self.data_loader = data_loader
        self.db = database
        
    def generate_exercises(self, chapter, exercise_type=None, count=5):
        """Генерация упражнений"""
        exercises = self.data_loader.get_exercises(chapter, exercise_type)
        random.shuffle(exercises)
        return exercises[:count]
    
    def generate_test(self, chapters, level, count=20):
        """Генерация теста по нескольким главам"""
        questions = []
        for chapter in chapters:
            exercises = self.data_loader.get_exercises(chapter)
            filtered = [e for e in exercises if e.level <= level]
            questions.extend(filtered)
        
        random.shuffle(questions)
        return questions[:count]
    
    def check_answer(self, exercise_id, user_answer):
        """Проверка ответа"""
        exercise = self.data_loader.get_exercise(exercise_id)
        is_correct = (user_answer == exercise.answer)
        return {
            'correct': is_correct,
            'explanation': exercise.explanation,
            'correct_answer': exercise.answer if not is_correct else None
        }
    
    def get_recommended_exercises(self, user_id):
        """Рекомендация упражнений на основе ошибок"""
        weak_points = self.db.get_user_weak_points(user_id)
        exercises = []
        for point in weak_points:
            ex = self.data_loader.get_exercises_by_topic(point)
            exercises.extend(ex)
        return exercises[:10]
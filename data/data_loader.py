"""
Загрузка всех данных из JSON файлов.
"""
class DataLoader:
    def __init__(self, data_file="japanese_data.json"):
        self.data_file = data_file
        self.data = {}
        
    def load_all(self):
        """Загрузка всех данных"""
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data
    
    def get_chapter_data(self, chapter):
        """Получение данных конкретной главы"""
        
    def get_vocabulary(self, filters=None):
        """Получение лексики с фильтрацией"""
        
    def get_grammar(self, filters=None):
        """Получение грамматики с фильтрацией"""
        
    def get_kanji(self, filters=None):
        """Получение кандзи с фильтрацией"""
        
    def get_exercises(self, chapter, exercise_type=None):
        """Получение упражнений"""
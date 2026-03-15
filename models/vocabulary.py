"""
Модель лексической единицы.
"""
class VocabularyItem:
    def __init__(self, word, reading, meaning, level, chapter, example=""):
        self.word = word
        self.reading = reading
        self.meaning = meaning
        self.level = level
        self.chapter = chapter
        self.example = example
        self.mastery = 0  # 0-100% уровень владения
        
    def to_dict(self):
        """Конвертация в словарь"""
        
    def update_mastery(self, correct):
        """Обновление уровня владения"""
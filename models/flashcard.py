"""
Модель флэшкарты для интервального повторения.
"""
class Flashcard:
    def __init__(self, id, user_id, word, reading, meaning, chapter, level):
        self.id = id
        self.user_id = user_id
        self.word = word
        self.reading = reading
        self.meaning = meaning
        self.chapter = chapter
        self.level = level
        self.ease_factor = 2.5  # фактор лёгкости (SM-2 алгоритм)
        self.interval = 0  # интервал в днях
        self.next_review = datetime.now()
        self.review_count = 0
        
    def update_review(self, quality):
        """
        Обновление карточки по алгоритму SM-2
        quality: 0-5 (0 - совсем забыл, 5 - идеально)
        """
        if quality >= 3:
            if self.review_count == 0:
                self.interval = 1
            elif self.review_count == 1:
                self.interval = 6
            else:
                self.interval = round(self.interval * self.ease_factor)
            
            self.review_count += 1
        else:
            self.interval = 0
            self.review_count = 0
        
        self.ease_factor = max(1.3, self.ease_factor + 0.1 - (5 - quality) * 0.08)
        self.next_review = datetime.now() + timedelta(days=self.interval)
"""
Сервис для работы с флэшкартами и интервальным повторением.
"""
class FlashcardService:
    def __init__(self, database):
        self.db = database
        
    def get_today_cards(self, user_id):
        """Получение карточек на сегодня"""
        query = """
            SELECT * FROM flashcards 
            WHERE user_id = ? AND date(next_review) <= date('now')
            ORDER BY next_review
        """
        results = self.db.execute_query(query, (user_id,))
        return [Flashcard(*row) for row in results]
    
    def add_card(self, user_id, word_data):
        """Добавление новой карточки"""
        card = Flashcard(
            user_id=user_id,
            word=word_data['word'],
            reading=word_data['reading'],
            meaning=word_data['meaning'],
            chapter=word_data['chapter'],
            level=word_data['level']
        )
        self.db.save_card(card)
        
    def update_card(self, card_id, quality):
        """Обновление карточки после ответа"""
        card = self.db.get_card(card_id)
        card.update_review(quality)
        self.db.update_card(card)
        
    def get_statistics(self, user_id):
        """Получение статистики"""
        stats = {
            'total': self.db.count_cards(user_id),
            'today': self.db.count_today_cards(user_id),
            'mastered': self.db.count_mastered_cards(user_id),
            'learning': self.db.count_learning_cards(user_id)
        }
        return stats
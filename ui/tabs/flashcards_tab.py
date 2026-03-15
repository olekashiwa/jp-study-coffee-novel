"""
Вкладка с флэшкартами для интервального повторения.
"""
class FlashcardsTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.current_card = None
        
        # Карточка
        self.card_widget = FlashcardWidget(self)
        
        # Кнопки управления
        self.control_frame = ttk.Frame(self)
        
        self.flip_btn = ttk.Button(
            self.control_frame,
            text="🔄 見る",
            command=self.flip_card
        )
        
        self.easy_btn = ttk.Button(
            self.control_frame,
            text="😊 簡単",
            command=lambda: self.rate_card(5)
        )
        
        self.good_btn = ttk.Button(
            self.control_frame,
            text="😐 普通",
            command=lambda: self.rate_card(3)
        )
        
        self.hard_btn = ttk.Button(
            self.control_frame,
            text="😓 難しい",
            command=lambda: self.rate_card(1)
        )
        
        # Статистика
        self.stats_label = ttk.Label(
            self,
            text="今日: 0 カード | 学習中: 0 | マスター: 0"
        )
        
        self.setup_layout()
        self.load_today_cards()
        
    def load_today_cards(self):
        """Загрузка карточек на сегодня"""
        cards = self.app.flashcard_service.get_today_cards()
        self.card_queue = cards
        self.show_next_card()
        
    def show_next_card(self):
        """Показать следующую карточку"""
        if self.card_queue:
            self.current_card = self.card_queue.pop(0)
            self.card_widget.set_front(self.current_card.word)
            self.card_widget.set_back(
                f"{self.current_card.reading}\n\n{self.current_card.meaning}"
            )
            self.update_stats()
        else:
            self.card_widget.set_message("今日のカードは終了しました！")
            
    def rate_card(self, quality):
        """Оценка карточки (SM-2 алгоритм)"""
        if self.current_card:
            self.app.flashcard_service.update_card(
                self.current_card.id,
                quality
            )
            self.show_next_card()
            
    def flip_card(self):
        """Перевернуть карточку"""
        self.card_widget.flip()
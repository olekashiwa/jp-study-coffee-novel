"""
Вкладка с лексикой.
"""
class VocabularyTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Фильтры
        self.filter_frame = FilterFrame(
            self,
            filters=["chapter", "level"],
            callback=self.apply_filters
        )
        
        # Таблица лексики
        self.table = VocabularyTable(self)
        
        # Детальная информация
        self.detail_frame = VocabularyDetail(self)
        
        # Кнопки действий
        self.action_frame = ttk.Frame(self)
        self.add_to_flashcards_btn = ttk.Button(
            self.action_frame,
            text="🃏 カードに追加",
            command=self.add_to_flashcards
        )
        self.export_btn = ttk.Button(
            self.action_frame,
            text="📤 エクスポート",
            command=self.export_vocab
        )
        
        self.setup_layout()
        self.load_data()
        
    def load_data(self):
        """Загрузка данных из DataLoader"""
        data = self.app.data_loader.get_vocabulary()
        self.table.populate(data)
        
    def apply_filters(self, filters):
        """Применение фильтров"""
        filtered = self.app.data_loader.get_vocabulary(filters)
        self.table.populate(filtered)
        
    def add_to_flashcards(self):
        """Добавление выбранных слов в флэшкарты"""
        selected = self.table.get_selected()
        self.app.flashcard_service.add_words(selected)
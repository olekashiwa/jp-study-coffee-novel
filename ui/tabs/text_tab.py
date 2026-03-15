"""
Вкладка с текстом главы.
"""
class TextTab(ttk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        
        # Выбор главы
        self.chapter_selector = ChapterSelector(self)
        
        # Область текста
        self.text_area = scrolledtext.ScrolledText(
            self, 
            font=('MS Mincho', 14),
            wrap=tk.WORD
        )
        
        # Область перевода
        self.translation_area = scrolledtext.ScrolledText(
            self,
            font=('Arial', 12),
            wrap=tk.WORD
        )
        
        # Область заметок
        self.notes_area = scrolledtext.ScrolledText(
            self,
            font=('Arial', 12),
            wrap=tk.WORD
        )
        
        # Кнопки
        self.save_notes_btn = ttk.Button(
            self,
            text="ノートを保存",
            command=self.save_notes
        )
        
        self.setup_layout()
        
    def setup_layout(self):
        """Настройка расположения элементов"""
        
    def load_chapter(self, chapter_key):
        """Загрузка текста главы"""
        
    def save_notes(self):
        """Сохранение заметок в БД"""
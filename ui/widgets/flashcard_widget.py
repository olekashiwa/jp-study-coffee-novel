"""
Виджет флэшкарты.
"""
class FlashcardWidget(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.front_text = tk.StringVar()
        self.back_text = tk.StringVar()
        self.is_flipped = False
        
        # Карточка
        self.card_frame = tk.Frame(
            self,
            bg='white',
            relief='raised',
            bd=2
        )
        
        self.card_label = tk.Label(
            self.card_frame,
            textvariable=self.front_text,
            font=('MS Mincho', 48),
            bg='white',
            wraplength=600
        )
        self.card_label.pack(expand=True, fill='both', padx=20, pady=20)
        
        self.setup_layout()
        
    def set_front(self, text):
        """Установка текста на лицевой стороне"""
        self.front_text.set(text)
        self.is_flipped = False
        
    def set_back(self, text):
        """Установка текста на обратной стороне"""
        self.back_text.set(text)
        
    def flip(self):
        """Переворот карточки"""
        if self.is_flipped:
            self.card_label.config(textvariable=self.front_text)
        else:
            self.card_label.config(textvariable=self.back_text)
        self.is_flipped = not self.is_flipped
"""
Главное окно приложения с Notebook.
"""
class MainWindow:
    def __init__(self, parent, app):
        self.parent = parent
        self.app = app
        self.notebook = ttk.Notebook(parent)
        
        # Создание вкладок
        self.text_tab = TextTab(self.notebook, app)
        self.vocab_tab = VocabularyTab(self.notebook, app)
        self.grammar_tab = GrammarTab(self.notebook, app)
        self.kanji_tab = KanjiTab(self.notebook, app)
        self.exercises_tab = ExercisesTab(self.notebook, app)
        self.flashcards_tab = FlashcardsTab(self.notebook, app)
        
        # Добавление вкладок
        self.notebook.add(self.text_tab, text="📖 テキスト")
        self.notebook.add(self.vocab_tab, text="📚 語彙")
        self.notebook.add(self.grammar_tab, text="🔤 文法")
        self.notebook.add(self.kanji_tab, text="🈳 漢字")
        self.notebook.add(self.exercises_tab, text="✍️ 練習問題")
        self.notebook.add(self.flashcards_tab, text="🃏 フラッシュカード")
        
        # Статус бар
        self.status_bar = StatusBar(parent)
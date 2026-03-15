"""
Приложение для изучения японского языка по роману «コーヒーが冷めないうちに»
Уровни: N3-N1
Функционал: работа с текстом, грамматика, лексика, иероглифика, тесты
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import random
import sqlite3
from datetime import datetime
import os

# ============== ОСНОВНОЙ КЛАСС ПРИЛОЖЕНИЯ ==============

class JapaneseLearningApp:
    def __init__(self, root):
        self.root = root
        self.root.title("日本語学習アプリ - コーヒーが冷めないうちに")
        self.root.geometry("1300x800")
        
        # Настройка базы данных
        self.setup_database()
        
        # Загрузка данных из JSON
        self.load_data()
        
        # Текущий пользователь и прогресс
        self.current_user = None
        self.current_lesson = 0
        self.current_exercise = 0
        self.score = 0
        
        # Создание интерфейса
        self.setup_ui()
        
    def setup_database(self):
        """Инициализация базы данных SQLite"""
        self.conn = sqlite3.connect('japanese_learning.db')
        self.cursor = self.conn.cursor()
        
        # Таблица пользователей
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                level TEXT,
                total_score INTEGER DEFAULT 0,
                created_at TIMESTAMP
            )
        ''')
        
        # Таблица прогресса
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                chapter TEXT,
                exercise_type TEXT,
                score INTEGER,
                completed_at TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Таблица для сохранения карточек
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS flashcards (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                word TEXT,
                reading TEXT,
                meaning TEXT,
                chapter TEXT,
                level TEXT,
                next_review TIMESTAMP,
                ease_factor REAL DEFAULT 2.5,
                interval INTEGER DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        self.conn.commit()
    
    def load_data(self):
        """Загрузка лингвистических данных из JSON"""
        # В реальном приложении здесь будет загрузка из файла
        # Для демонстрации создадим структуру данных
        
        self.chapters = {
            "prologue": {
                "title": "プロローグ - 喫茶店のルール",
                "level": "N3",
                "text": self.load_chapter_text("prologue"),
                "vocabulary": self.load_chapter_vocab("prologue"),
                "grammar": self.load_chapter_grammar("prologue"),
                "kanji": self.load_chapter_kanji("prologue"),
                "exercises": self.load_chapter_exercises("prologue")
            },
            "chapter1": {
                "title": "第一話『恋人』",
                "level": "N3-N2",
                "text": self.load_chapter_text("chapter1"),
                "vocabulary": self.load_chapter_vocab("chapter1"),
                "grammar": self.load_chapter_grammar("chapter1"),
                "kanji": self.load_chapter_kanji("chapter1"),
                "exercises": self.load_chapter_exercises("chapter1")
            },
            "chapter2": {
                "title": "第二話『夫婦』",
                "level": "N2",
                "text": self.load_chapter_text("chapter2"),
                "vocabulary": self.load_chapter_vocab("chapter2"),
                "grammar": self.load_chapter_grammar("chapter2"),
                "kanji": self.load_chapter_kanji("chapter2"),
                "exercises": self.load_chapter_exercises("chapter2")
            },
            "chapter3": {
                "title": "第三話『姉妹』",
                "level": "N2",
                "text": self.load_chapter_text("chapter3"),
                "vocabulary": self.load_chapter_vocab("chapter3"),
                "grammar": self.load_chapter_grammar("chapter3"),
                "kanji": self.load_chapter_kanji("chapter3"),
                "exercises": self.load_chapter_exercises("chapter3")
            },
            "chapter4": {
                "title": "第四話『親子』",
                "level": "N2-N1",
                "text": self.load_chapter_text("chapter4"),
                "vocabulary": self.load_chapter_vocab("chapter4"),
                "grammar": self.load_chapter_grammar("chapter4"),
                "kanji": self.load_chapter_kanji("chapter4"),
                "exercises": self.load_chapter_exercises("chapter4")
            }
        }
    
    def load_chapter_text(self, chapter):
        """Загрузка текста главы"""
        texts = {
            "prologue": """とある街の、とある喫茶店のとある席には不思議な都市伝説があった。
その席に座ると、その席に座っている間だけ望んだ通りの時間に移動ができるという。
ただし、そこにはめんどくさい……非常にめんどくさいルールがあった。

一、過去に戻っても、この喫茶店を訪れた事のない者には会う事ができない。
二、過去に戻ってどんな努力をしても、現実は変わらない。
三、過去に戻れる席には先客がいる。席に座れるのは、その先客が席を立った時だけ。
四、過去に戻っても、席を立って移動する事はできない。
五、過去に戻れるのは、コーヒーをカップに注いでから、そのコーヒーが冷めてしまうまでの間だけ。""",
            
            "chapter1": """「じゃ、俺、時間なんで......」歯切れの悪いぼそぼそ声でそう言うと、男はキャリーバッグに手をのばしながら立ち上がった。
「え？」女は男の顔を見上げて怪訝そうな顔をゆがめた。""",
            
            "chapter2": """房木は毎日のようにこの喫茶店を訪れ、旅行雑誌を広げてノートにメモを取っている。
四十路を越えた男で、髪は短く刈り込み、白髪が目立つ。眼鏡をかけた顔は疲れた表情だ。""",
            
            "chapter3": """平井久美は、姉の八絵子に会うため、東京へやってきた。
「すみません、姉は来てませんか？」久美はカウンターの数に尋ねた。""",
            
            "chapter4": """この喫茶店のマスター、時田流は数の従兄であり、夫でもある。
数が幼い頃、彼女の両親は離婚した。父親は彼女を置いて家を出て行った。"""
        }
        return texts.get(chapter, "")
    
    def load_chapter_vocab(self, chapter):
        """Загрузка лексики главы"""
        vocab = {
            "prologue": [
                {"word": "都市伝説", "reading": "としでんせつ", "meaning": "городская легенда", "level": "N3"},
                {"word": "過去", "reading": "かこ", "meaning": "прошлое", "level": "N3"},
                {"word": "現実", "reading": "げんじつ", "meaning": "реальность", "level": "N2"},
                {"word": "先客", "reading": "せんきゃく", "meaning": "предыдущий гость", "level": "N2"},
                {"word": "めんどくさい", "reading": "", "meaning": "хлопотный", "level": "N3"}
            ],
            "chapter1": [
                {"word": "彼氏", "reading": "かれし", "meaning": "парень", "level": "N3"},
                {"word": "別れ", "reading": "わかれ", "meaning": "расставание", "level": "N2"},
                {"word": "怪訝", "reading": "けげん", "meaning": "удивлённый", "level": "N2"},
                {"word": "プライド", "reading": "", "meaning": "гордость", "level": "N2"},
                {"word": "歯切れ悪い", "reading": "はぎれわるい", "meaning": "невнятный", "level": "N2"}
            ]
        }
        return vocab.get(chapter, [])
    
    def load_chapter_grammar(self, chapter):
        """Загрузка грамматики главы"""
        grammar = {
            "prologue": [
                {"pattern": "〜ても", "meaning": "даже если", "example": "戻っても現実は変わらない", "level": "N3"},
                {"pattern": "〜てしまう", "meaning": "завершённость", "example": "冷めてしまう", "level": "N3"},
                {"pattern": "どんな〜も", "meaning": "любой", "example": "どんな努力をしても", "level": "N2"}
            ],
            "chapter1": [
                {"pattern": "〜ながら", "meaning": "одновременность", "example": "手をのばしながら", "level": "N2"},
                {"pattern": "〜そうだ", "meaning": "выглядит как", "example": "悲しそうな顔", "level": "N3"},
                {"pattern": "〜つもり", "meaning": "намерение", "example": "言わせるつもり", "level": "N3"}
            ]
        }
        return grammar.get(chapter, [])
    
    def load_chapter_kanji(self, chapter):
        """Загрузка иероглифов главы"""
        kanji = {
            "prologue": [
                {"kanji": "都", "reading": "と, みやこ", "meaning": "столица", "examples": "都市"},
                {"kanji": "市", "reading": "し, いち", "meaning": "город", "examples": "都市"},
                {"kanji": "伝", "reading": "でん, つたえる", "meaning": "передавать", "examples": "伝説"},
                {"kanji": "説", "reading": "せつ, とく", "meaning": "объяснение", "examples": "伝説"},
                {"kanji": "過", "reading": "か, すごす", "meaning": "проходить", "examples": "過去"}
            ],
            "chapter1": [
                {"kanji": "彼", "reading": "かれ, ひ", "meaning": "он", "examples": "彼氏"},
                {"kanji": "氏", "reading": "し, うじ", "meaning": "господин", "examples": "彼氏"},
                {"kanji": "別", "reading": "べつ, わかれる", "meaning": "отдельный", "examples": "別れ"},
                {"kanji": "怪", "reading": "かい, あやしい", "meaning": "подозрительный", "examples": "怪訝"},
                {"kanji": "訝", "reading": "げん, いぶかる", "meaning": "сомневаться", "examples": "怪訝"}
            ]
        }
        return kanji.get(chapter, [])
    
    def load_chapter_exercises(self, chapter):
        """Загрузка упражнений главы"""
        exercises = {
            "prologue": [
                {
                    "type": "grammar",
                    "question": "過去に戻っ___、現実は変わらない。",
                    "options": ["ても", "たら", "と", "ば"],
                    "answer": "ても",
                    "explanation": "〜ても - даже если"
                },
                {
                    "type": "vocab",
                    "question": "「めんどくさい」の意味は？",
                    "options": ["интересный", "хлопотный", "вкусный", "красивый"],
                    "answer": "хлопотный",
                    "explanation": "面倒くさい - хлопотный, надоедливый"
                },
                {
                    "type": "kanji",
                    "question": "「過去」の読み方は？",
                    "options": ["かこ", "みらい", "げんざい", "じかん"],
                    "answer": "かこ",
                    "explanation": "過去 - прошлое"
                }
            ],
            "chapter1": [
                {
                    "type": "grammar",
                    "question": "彼はコーヒーを飲み___席を立った。",
                    "options": ["ながら", "ても", "たり", "てから"],
                    "answer": "ながら",
                    "explanation": "〜ながら - одновременность действий"
                },
                {
                    "type": "vocab",
                    "question": "「彼氏」の意味は？",
                    "options": ["подруга", "парень", "муж", "друг"],
                    "answer": "парень",
                    "explanation": "彼氏 - парень (романтический партнёр)"
                }
            ]
        }
        return exercises.get(chapter, [])
    
    def setup_ui(self):
        """Создание пользовательского интерфейса"""
        
        # Главное меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ファイル", menu=file_menu)
        file_menu.add_command(label="ログイン", command=self.show_login)
        file_menu.add_command(label="ユーザー登録", command=self.show_register)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.root.quit)
        
        # Меню "Обучение"
        study_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="学習", menu=study_menu)
        study_menu.add_command(label="テキスト", command=self.show_text)
        study_menu.add_command(label="語彙", command=self.show_vocabulary)
        study_menu.add_command(label="文法", command=self.show_grammar)
        study_menu.add_command(label="漢字", command=self.show_kanji)
        study_menu.add_command(label="練習問題", command=self.show_exercises)
        
        # Меню "Инструменты"
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ツール", menu=tools_menu)
        tools_menu.add_command(label="フラッシュカード", command=self.show_flashcards)
        tools_menu.add_command(label="テスト", command=self.show_test)
        tools_menu.add_command(label="進捗状況", command=self.show_progress)
        
        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ヘルプ", menu=help_menu)
        help_menu.add_command(label="使い方", command=self.show_help)
        help_menu.add_command(label="について", command=self.show_about)
        
        # Основной контейнер с вкладками
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка 1: Текст
        self.tab_text = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_text, text="📖 テキスト")
        self.setup_text_tab()
        
        # Вкладка 2: Лексика
        self.tab_vocab = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_vocab, text="📚 語彙")
        self.setup_vocab_tab()
        
        # Вкладка 3: Грамматика
        self.tab_grammar = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_grammar, text="🔤 文法")
        self.setup_grammar_tab()
        
        # Вкладка 4: Кандзи
        self.tab_kanji = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_kanji, text="🈳 漢字")
        self.setup_kanji_tab()
        
        # Вкладка 5: Упражнения
        self.tab_exercises = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_exercises, text="✍️ 練習問題")
        self.setup_exercises_tab()
        
        # Вкладка 6: Флэшкарты
        self.tab_flashcards = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_flashcards, text="🃏 フラッシュカード")
        self.setup_flashcards_tab()
        
        # Статус бар
        self.status_var = tk.StringVar()
        self.status_var.set("ようこそ！ログインしてください。")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, 
                               relief='sunken', anchor='w')
        status_bar.pack(fill='x', padx=10, pady=(0,10))
    
    def setup_text_tab(self):
        """Вкладка с текстом глав"""
        
        # Верхняя панель - выбор главы
        top_frame = ttk.Frame(self.tab_text)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(top_frame, text="章を選択:", font=('Arial', 11)).pack(side='left', padx=(0,10))
        
        self.text_chapter_var = tk.StringVar()
        self.text_chapter_combo = ttk.Combobox(top_frame, textvariable=self.text_chapter_var,
                                               values=["プロローグ", "第一話『恋人』", "第二話『夫婦』", 
                                                      "第三話『姉妹』", "第四話『親子』"],
                                               state='readonly', width=20)
        self.text_chapter_combo.pack(side='left', padx=(0,10))
        self.text_chapter_combo.bind('<<ComboboxSelected>>', self.on_chapter_selected)
        
        ttk.Button(top_frame, text="表示", command=self.display_text).pack(side='left')
        
        # Область текста
        text_frame = ttk.LabelFrame(self.tab_text, text="原文", padding="10")
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.text_display = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD,
                                                      font=('MS Mincho', 14), height=15)
        self.text_display.pack(fill='both', expand=True)
        
        # Область перевода и заметок
        bottom_frame = ttk.Frame(self.tab_text)
        bottom_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Левая панель - перевод
        trans_frame = ttk.LabelFrame(bottom_frame, text="翻訳", padding="10")
        trans_frame.pack(side='left', fill='both', expand=True, padx=(0,5))
        
        self.translation_display = scrolledtext.ScrolledText(trans_frame, wrap=tk.WORD,
                                                              font=('Arial', 12), height=10)
        self.translation_display.pack(fill='both', expand=True)
        
        # Правая панель - заметки
        notes_frame = ttk.LabelFrame(bottom_frame, text="ノート", padding="10")
        notes_frame.pack(side='right', fill='both', expand=True, padx=(5,0))
        
        self.notes_display = scrolledtext.ScrolledText(notes_frame, wrap=tk.WORD,
                                                        font=('Arial', 12), height=10)
        self.notes_display.pack(fill='both', expand=True)
    
    def setup_vocab_tab(self):
        """Вкладка с лексикой"""
        
        # Верхняя панель - фильтры
        filter_frame = ttk.Frame(self.tab_vocab)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filter_frame, text="章:").pack(side='left', padx=(0,5))
        self.vocab_chapter_var = tk.StringVar()
        vocab_chapter_combo = ttk.Combobox(filter_frame, textvariable=self.vocab_chapter_var,
                                           values=["すべて", "プロローグ", "第一話", "第二話", "第三話", "第四話"],
                                           state='readonly', width=15)
        vocab_chapter_combo.pack(side='left', padx=(0,10))
        vocab_chapter_combo.bind('<<ComboboxSelected>>', self.filter_vocab)
        
        ttk.Label(filter_frame, text="レベル:").pack(side='left', padx=(0,5))
        self.vocab_level_var = tk.StringVar()
        vocab_level_combo = ttk.Combobox(filter_frame, textvariable=self.vocab_level_var,
                                         values=["すべて", "N3", "N2", "N1"],
                                         state='readonly', width=10)
        vocab_level_combo.pack(side='left', padx=(0,10))
        vocab_level_combo.bind('<<ComboboxSelected>>', self.filter_vocab)
        
        ttk.Button(filter_frame, text="フィルター", command=self.filter_vocab).pack(side='left', padx=(0,5))
        ttk.Button(filter_frame, text="カードに追加", command=self.add_to_flashcards).pack(side='left')
        
        # Таблица лексики
        table_frame = ttk.LabelFrame(self.tab_vocab, text="語彙リスト", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Создаём Treeview для отображения лексики
        columns = ('word', 'reading', 'meaning', 'level', 'chapter')
        self.vocab_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        self.vocab_tree.heading('word', text='単語')
        self.vocab_tree.heading('reading', text='読み方')
        self.vocab_tree.heading('meaning', text='意味')
        self.vocab_tree.heading('level', text='レベル')
        self.vocab_tree.heading('chapter', text='章')
        
        self.vocab_tree.column('word', width=150)
        self.vocab_tree.column('reading', width=150)
        self.vocab_tree.column('meaning', width=250)
        self.vocab_tree.column('level', width=80)
        self.vocab_tree.column('chapter', width=100)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.vocab_tree.yview)
        self.vocab_tree.configure(yscrollcommand=scrollbar.set)
        
        self.vocab_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Привязываем событие выбора
        self.vocab_tree.bind('<<TreeviewSelect>>', self.on_vocab_selected)
        
        # Нижняя панель - детали
        detail_frame = ttk.LabelFrame(self.tab_vocab, text="詳細", padding="10")
        detail_frame.pack(fill='x', padx=10, pady=10)
        
        self.vocab_detail = scrolledtext.ScrolledText(detail_frame, wrap=tk.WORD,
                                                       font=('Arial', 11), height=5)
        self.vocab_detail.pack(fill='both', expand=True)
    
    def setup_grammar_tab(self):
        """Вкладка с грамматикой"""
        
        # Верхняя панель - фильтры
        filter_frame = ttk.Frame(self.tab_grammar)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filter_frame, text="章:").pack(side='left', padx=(0,5))
        self.grammar_chapter_var = tk.StringVar()
        grammar_chapter_combo = ttk.Combobox(filter_frame, textvariable=self.grammar_chapter_var,
                                             values=["すべて", "プロローグ", "第一話", "第二話", "第三話", "第四話"],
                                             state='readonly', width=15)
        grammar_chapter_combo.pack(side='left', padx=(0,10))
        grammar_chapter_combo.bind('<<ComboboxSelected>>', self.filter_grammar)
        
        ttk.Label(filter_frame, text="レベル:").pack(side='left', padx=(0,5))
        self.grammar_level_var = tk.StringVar()
        grammar_level_combo = ttk.Combobox(filter_frame, textvariable=self.grammar_level_var,
                                           values=["すべて", "N3", "N2", "N1"],
                                           state='readonly', width=10)
        grammar_level_combo.pack(side='left', padx=(0,10))
        grammar_level_combo.bind('<<ComboboxSelected>>', self.filter_grammar)
        
        ttk.Button(filter_frame, text="フィルター", command=self.filter_grammar).pack(side='left')
        
        # Таблица грамматики
        table_frame = ttk.LabelFrame(self.tab_grammar, text="文法リスト", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('pattern', 'meaning', 'example', 'level', 'chapter')
        self.grammar_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        self.grammar_tree.heading('pattern', text='文法')
        self.grammar_tree.heading('meaning', text='意味')
        self.grammar_tree.heading('example', text='例文')
        self.grammar_tree.heading('level', text='レベル')
        self.grammar_tree.heading('chapter', text='章')
        
        self.grammar_tree.column('pattern', width=150)
        self.grammar_tree.column('meaning', width=200)
        self.grammar_tree.column('example', width=300)
        self.grammar_tree.column('level', width=80)
        self.grammar_tree.column('chapter', width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.grammar_tree.yview)
        self.grammar_tree.configure(yscrollcommand=scrollbar.set)
        
        self.grammar_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.grammar_tree.bind('<<TreeviewSelect>>', self.on_grammar_selected)
    
    def setup_kanji_tab(self):
        """Вкладка с иероглифами"""
        
        # Верхняя панель - фильтры
        filter_frame = ttk.Frame(self.tab_kanji)
        filter_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(filter_frame, text="章:").pack(side='left', padx=(0,5))
        self.kanji_chapter_var = tk.StringVar()
        kanji_chapter_combo = ttk.Combobox(filter_frame, textvariable=self.kanji_chapter_var,
                                           values=["すべて", "プロローグ", "第一話", "第二話", "第三話", "第四話"],
                                           state='readonly', width=15)
        kanji_chapter_combo.pack(side='left', padx=(0,10))
        kanji_chapter_combo.bind('<<ComboboxSelected>>', self.filter_kanji)
        
        ttk.Entry(filter_frame, width=20).pack(side='left', padx=(0,10))
        ttk.Button(filter_frame, text="検索", command=self.search_kanji).pack(side='left')
        
        ttk.Button(filter_frame, text="フィルター", command=self.filter_kanji).pack(side='left', padx=(10,0))
        
        # Таблица кандзи
        table_frame = ttk.LabelFrame(self.tab_kanji, text="漢字リスト", padding="10")
        table_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        columns = ('kanji', 'reading', 'meaning', 'examples', 'chapter')
        self.kanji_tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        self.kanji_tree.heading('kanji', text='漢字')
        self.kanji_tree.heading('reading', text='読み方')
        self.kanji_tree.heading('meaning', text='意味')
        self.kanji_tree.heading('examples', text='例')
        self.kanji_tree.heading('chapter', text='章')
        
        self.kanji_tree.column('kanji', width=80)
        self.kanji_tree.column('reading', width=200)
        self.kanji_tree.column('meaning', width=150)
        self.kanji_tree.column('examples', width=200)
        self.kanji_tree.column('chapter', width=100)
        
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=self.kanji_tree.yview)
        self.kanji_tree.configure(yscrollcommand=scrollbar.set)
        
        self.kanji_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.kanji_tree.bind('<<TreeviewSelect>>', self.on_kanji_selected)
    
    def setup_exercises_tab(self):
        """Вкладка с упражнениями"""
        
        # Верхняя панель - выбор упражнения
        top_frame = ttk.Frame(self.tab_exercises)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(top_frame, text="章を選択:", font=('Arial', 11)).pack(side='left', padx=(0,10))
        
        self.ex_chapter_var = tk.StringVar()
        ex_chapter_combo = ttk.Combobox(top_frame, textvariable=self.ex_chapter_var,
                                        values=["プロローグ", "第一話", "第二話", "第三話", "第四話"],
                                        state='readonly', width=15)
        ex_chapter_combo.pack(side='left', padx=(0,10))
        ex_chapter_combo.bind('<<ComboboxSelected>>', self.load_exercises)
        
        ttk.Label(top_frame, text="問題タイプ:", font=('Arial', 11)).pack(side='left', padx=(10,5))
        self.ex_type_var = tk.StringVar()
        ex_type_combo = ttk.Combobox(top_frame, textvariable=self.ex_type_var,
                                     values=["すべて", "文法", "語彙", "漢字"],
                                     state='readonly', width=10)
        ex_type_combo.pack(side='left', padx=(0,10))
        ex_type_combo.bind('<<ComboboxSelected>>', self.load_exercises)
        
        ttk.Button(top_frame, text="開始", command=self.start_exercise).pack(side='left')
        
        # Основная область - вопрос
        question_frame = ttk.LabelFrame(self.tab_exercises, text="問題", padding="10")
        question_frame.pack(fill='x', padx=10, pady=10)
        
        self.question_text = tk.StringVar()
        ttk.Label(question_frame, textvariable=self.question_text, font=('Arial', 12),
                  wraplength=1000).pack(anchor='w')
        
        # Варианты ответов
        options_frame = ttk.LabelFrame(self.tab_exercises, text="選択肢", padding="10")
        options_frame.pack(fill='x', padx=10, pady=10)
        
        self.option_vars = []
        self.option_buttons = []
        
        for i in range(4):
            var = tk.StringVar()
            self.option_vars.append(var)
            
            rb = ttk.Radiobutton(options_frame, textvariable=var, value=var.get(),
                                 variable=self.selected_option)
            rb.pack(anchor='w', pady=2)
            self.option_buttons.append(rb)
        
        # Кнопки
        button_frame = ttk.Frame(self.tab_exercises)
        button_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(button_frame, text="回答", command=self.check_answer).pack(side='left', padx=5)
        ttk.Button(button_frame, text="次へ", command=self.next_question).pack(side='left', padx=5)
        ttk.Button(button_frame, text="ヒント", command=self.show_hint).pack(side='left', padx=5)
        
        # Область результата
        result_frame = ttk.LabelFrame(self.tab_exercises, text="結果", padding="10")
        result_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD,
                                                      font=('Arial', 11), height=5)
        self.result_text.pack(fill='both', expand=True)
        
        # Счет
        score_frame = ttk.Frame(self.tab_exercises)
        score_frame.pack(fill='x', padx=10, pady=(0,10))
        
        self.score_var = tk.StringVar(value="スコア: 0/0")
        ttk.Label(score_frame, textvariable=self.score_var, font=('Arial', 11, 'bold')).pack(side='right')
    
    def setup_flashcards_tab(self):
        """Вкладка с флэшкартами"""
        
        # Верхняя панель - управление
        top_frame = ttk.Frame(self.tab_flashcards)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(top_frame, text="新しいカード", command=self.add_new_card).pack(side='left', padx=5)
        ttk.Button(top_frame, text="今日のカード", command=self.show_today_cards).pack(side='left', padx=5)
        ttk.Button(top_frame, text="すべてのカード", command=self.show_all_cards).pack(side='left', padx=5)
        ttk.Button(top_frame, text="復習", command=self.start_review).pack(side='left', padx=5)
        
        # Карточка
        card_frame = ttk.LabelFrame(self.tab_flashcards, text="カード", padding="20")
        card_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        self.card_front = tk.StringVar(value="表")
        self.card_back = tk.StringVar(value="裏")
        
        self.card_label = tk.Label(card_frame, textvariable=self.card_front, font=('MS Mincho', 48),
                                    bg='white', relief='raised', height=6)
        self.card_label.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Кнопки для ответа
        answer_frame = ttk.Frame(self.tab_flashcards)
        answer_frame.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(answer_frame, text="見る", command=self.flip_card).pack(side='left', padx=5)
        ttk.Button(answer_frame, text="簡単", command=self.easy_card).pack(side='left', padx=5)
        ttk.Button(answer_frame, text="普通", command=self.good_card).pack(side='left', padx=5)
        ttk.Button(answer_frame, text="難しい", command=self.hard_card).pack(side='left', padx=5)
        
        # Статистика
        stats_frame = ttk.Frame(self.tab_flashcards)
        stats_frame.pack(fill='x', padx=10, pady=(0,10))
        
        self.card_stats = tk.StringVar(value="今日: 0 カード")
        ttk.Label(stats_frame, textvariable=self.card_stats).pack(side='right')
    
    # ============== МЕТОДЫ ДЛЯ РАБОТЫ ==============
    
    def show_login(self):
        """Окно входа в систему"""
        login_window = tk.Toplevel(self.root)
        login_window.title("ログイン")
        login_window.geometry("300x200")
        login_window.resizable(False, False)
        
        ttk.Label(login_window, text="ユーザー名:").pack(pady=(20,5))
        username_entry = ttk.Entry(login_window, width=30)
        username_entry.pack(pady=5)
        
        def login():
            username = username_entry.get()
            if username:
                self.cursor.execute("SELECT id, username, level FROM users WHERE username=?", (username,))
                user = self.cursor.fetchone()
                
                if user:
                    self.current_user = {"id": user[0], "username": user[1], "level": user[2]}
                    self.status_var.set(f"ようこそ、{username}さん！")
                    login_window.destroy()
                    
                    # Загружаем прогресс
                    self.load_user_progress()
                else:
                    messagebox.showerror("エラー", "ユーザーが見つかりません。")
            else:
                messagebox.showwarning("警告", "ユーザー名を入力してください。")
        
        ttk.Button(login_window, text="ログイン", command=login).pack(pady=20)
    
    def show_register(self):
        """Окно регистрации"""
        register_window = tk.Toplevel(self.root)
        register_window.title("ユーザー登録")
        register_window.geometry("300x250")
        register_window.resizable(False, False)
        
        ttk.Label(register_window, text="ユーザー名:").pack(pady=(20,5))
        username_entry = ttk.Entry(register_window, width=30)
        username_entry.pack(pady=5)
        
        ttk.Label(register_window, text="レベル:").pack(pady=5)
        level_combo = ttk.Combobox(register_window, values=["N3", "N2", "N1"], state='readonly')
        level_combo.pack(pady=5)
        level_combo.set("N3")
        
        def register():
            username = username_entry.get()
            level = level_combo.get()
            
            if username and level:
                try:
                    self.cursor.execute(
                        "INSERT INTO users (username, level, created_at) VALUES (?, ?, ?)",
                        (username, level, datetime.now())
                    )
                    self.conn.commit()
                    messagebox.showinfo("成功", "登録が完了しました！")
                    register_window.destroy()
                except sqlite3.IntegrityError:
                    messagebox.showerror("エラー", "このユーザー名は既に使われています。")
            else:
                messagebox.showwarning("警告", "全ての項目を入力してください。")
        
        ttk.Button(register_window, text="登録", command=register).pack(pady=20)
    
    def load_user_progress(self):
        """Загрузка прогресса пользователя"""
        if not self.current_user:
            return
        
        self.cursor.execute(
            "SELECT SUM(score) FROM progress WHERE user_id=?",
            (self.current_user["id"],)
        )
        total = self.cursor.fetchone()[0]
        if total:
            self.current_user["total_score"] = total
    
    def display_text(self):
        """Отображение текста выбранной главы"""
        chapter = self.text_chapter_var.get()
        
        if not chapter:
            return
        
        chapter_key = {
            "プロローグ": "prologue",
            "第一話『恋人』": "chapter1",
            "第二話『夫婦』": "chapter2",
            "第三話『姉妹』": "chapter3",
            "第四話『親子』": "chapter4"
        }.get(chapter, "prologue")
        
        # Очищаем поля
        self.text_display.delete(1.0, tk.END)
        self.translation_display.delete(1.0, tk.END)
        
        # Вставляем текст
        if chapter_key in self.chapters:
            self.text_display.insert(tk.END, self.chapters[chapter_key]["text"])
            
            # Здесь должен быть перевод
            self.translation_display.insert(tk.END, f"[Перевод главы {chapter} будет здесь]")
    
    def filter_vocab(self, event=None):
        """Фильтрация лексики"""
        # Очищаем таблицу
        for row in self.vocab_tree.get_children():
            self.vocab_tree.delete(row)
        
        chapter_filter = self.vocab_chapter_var.get()
        level_filter = self.vocab_level_var.get()
        
        for chap_key, chap_data in self.chapters.items():
            chap_name = {
                "prologue": "プロローグ",
                "chapter1": "第一話",
                "chapter2": "第二話",
                "chapter3": "第三話",
                "chapter4": "第四話"
            }.get(chap_key, "")
            
            # Пропускаем, если не подходит по главе
            if chapter_filter != "すべて" and chapter_filter != chap_name:
                continue
            
            for vocab in chap_data["vocabulary"]:
                # Пропускаем, если не подходит по уровню
                if level_filter != "すべて" and level_filter != vocab["level"]:
                    continue
                
                self.vocab_tree.insert('', 'end', values=(
                    vocab["word"],
                    vocab.get("reading", ""),
                    vocab["meaning"],
                    vocab["level"],
                    chap_name
                ))
    
    def filter_grammar(self, event=None):
        """Фильтрация грамматики"""
        # Очищаем таблицу
        for row in self.grammar_tree.get_children():
            self.grammar_tree.delete(row)
        
        chapter_filter = self.grammar_chapter_var.get()
        level_filter = self.grammar_level_var.get()
        
        for chap_key, chap_data in self.chapters.items():
            chap_name = {
                "prologue": "プロローグ",
                "chapter1": "第一話",
                "chapter2": "第二話",
                "chapter3": "第三話",
                "chapter4": "第四話"
            }.get(chap_key, "")
            
            if chapter_filter != "すべて" and chapter_filter != chap_name:
                continue
            
            for grammar in chap_data["grammar"]:
                if level_filter != "すべて" and level_filter != grammar["level"]:
                    continue
                
                self.grammar_tree.insert('', 'end', values=(
                    grammar["pattern"],
                    grammar["meaning"],
                    grammar["example"],
                    grammar["level"],
                    chap_name
                ))
    
    def filter_kanji(self, event=None):
        """Фильтрация кандзи"""
        # Очищаем таблицу
        for row in self.kanji_tree.get_children():
            self.kanji_tree.delete(row)
        
        chapter_filter = self.kanji_chapter_var.get()
        
        for chap_key, chap_data in self.chapters.items():
            chap_name = {
                "prologue": "プロローグ",
                "chapter1": "第一話",
                "chapter2": "第二話",
                "chapter3": "第三話",
                "chapter4": "第四話"
            }.get(chap_key, "")
            
            if chapter_filter != "すべて" and chapter_filter != chap_name:
                continue
            
            for kanji in chap_data["kanji"]:
                self.kanji_tree.insert('', 'end', values=(
                    kanji["kanji"],
                    kanji["reading"],
                    kanji["meaning"],
                    kanji["examples"],
                    chap_name
                ))
    
    def search_kanji(self):
        """Поиск кандзи"""
        # Заглушка
        messagebox.showinfo("情報", "検索機能は現在開発中です。")
    
    def load_exercises(self, event=None):
        """Загрузка упражнений для выбранной главы"""
        chapter = self.ex_chapter_var.get()
        ex_type = self.ex_type_var.get()
        
        # Заглушка
        self.status_var.set(f"章: {chapter}, タイプ: {ex_type} の練習問題を読み込みました。")
    
    def start_exercise(self):
        """Начало упражнения"""
        chapter = self.ex_chapter_var.get()
        
        if not chapter:
            messagebox.showwarning("警告", "章を選択してください。")
            return
        
        chapter_key = {
            "プロローグ": "prologue",
            "第一話": "chapter1",
            "第二話": "chapter2",
            "第三話": "chapter3",
            "第四話": "chapter4"
        }.get(chapter, "prologue")
        
        exercises = self.chapters[chapter_key]["exercises"]
        
        if exercises:
            self.current_exercise = 0
            self.exercises = exercises
            self.total_exercises = len(exercises)
            self.show_question(0)
        else:
            messagebox.showinfo("情報", "この章には練習問題がありません。")
    
    def show_question(self, index):
        """Отображение вопроса"""
        if index < len(self.exercises):
            ex = self.exercises[index]
            self.question_text.set(f"問題 {index+1}/{self.total_exercises}: {ex['question']}")
            
            # Устанавливаем варианты
            for i, option in enumerate(ex["options"]):
                if i < len(self.option_vars):
                    self.option_vars[i].set(option)
            
            self.current_answer = ex["answer"]
            self.current_explanation = ex.get("explanation", "")
            
            # Очищаем результат
            self.result_text.delete(1.0, tk.END)
    
    def check_answer(self):
        """Проверка ответа"""
        selected = self.selected_option.get()
        
        if not selected:
            messagebox.showwarning("警告", "回答を選んでください。")
            return
        
        self.result_text.delete(1.0, tk.END)
        
        if selected == self.current_answer:
            self.result_text.insert(tk.END, "✅ 正解です！\n\n")
            self.score += 1
        else:
            self.result_text.insert(tk.END, f"❌ 不正解です。\n正解: {self.current_answer}\n\n")
        
        self.result_text.insert(tk.END, f"解説: {self.current_explanation}")
        self.score_var.set(f"スコア: {self.score}/{self.total_exercises}")
    
    def next_question(self):
        """Следующий вопрос"""
        if self.current_exercise + 1 < len(self.exercises):
            self.current_exercise += 1
            self.show_question(self.current_exercise)
        else:
            # Сохраняем результат
            if self.current_user:
                self.cursor.execute(
                    "INSERT INTO progress (user_id, chapter, exercise_type, score, completed_at) VALUES (?, ?, ?, ?, ?)",
                    (self.current_user["id"], self.ex_chapter_var.get(), "練習問題", self.score, datetime.now())
                )
                self.conn.commit()
            
            messagebox.showinfo("完了", f"おめでとうございます！全問題が終了しました。\n最終スコア: {self.score}/{self.total_exercises}")
            self.score = 0
            self.current_exercise = 0
            self.score_var.set("スコア: 0/0")
    
    def show_hint(self):
        """Показать подсказку"""
        if hasattr(self, 'current_answer'):
            messagebox.showinfo("ヒント", f"答えの最初の文字: {self.current_answer[0]}")
    
    def on_chapter_selected(self, event):
        """Обработка выбора главы"""
        pass
    
    def on_vocab_selected(self, event):
        """Обработка выбора лексики"""
        selection = self.vocab_tree.selection()
        if selection:
            item = self.vocab_tree.item(selection[0])
            values = item['values']
            
            self.vocab_detail.delete(1.0, tk.END)
            self.vocab_detail.insert(tk.END, f"単語: {values[0]}\n")
            self.vocab_detail.insert(tk.END, f"読み方: {values[1]}\n")
            self.vocab_detail.insert(tk.END, f"意味: {values[2]}\n")
            self.vocab_detail.insert(tk.END, f"レベル: {values[3]}\n")
            self.vocab_detail.insert(tk.END, f"章: {values[4]}\n")
    
    def on_grammar_selected(self, event):
        """Обработка выбора грамматики"""
        selection = self.grammar_tree.selection()
        if selection:
            item = self.grammar_tree.item(selection[0])
            values = item['values']
            
            # Здесь можно показать детали
            pass
    
    def on_kanji_selected(self, event):
        """Обработка выбора кандзи"""
        selection = self.kanji_tree.selection()
        if selection:
            item = self.kanji_tree.item(selection[0])
            values = item['values']
            
            # Здесь можно показать детали
            pass
    
    def add_to_flashcards(self):
        """Добавление выбранных слов в флэшкарты"""
        selection = self.vocab_tree.selection()
        
        if not selection:
            messagebox.showwarning("警告", "カードに追加する単語を選んでください。")
            return
        
        if not self.current_user:
            messagebox.showwarning("警告", "まずログインしてください。")
            return
        
        added = 0
        for sel in selection:
            item = self.vocab_tree.item(sel)
            values = item['values']
            
            self.cursor.execute(
                """INSERT INTO flashcards 
                   (user_id, word, reading, meaning, chapter, level, next_review) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                (self.current_user["id"], values[0], values[1], values[2], values[4], values[3], datetime.now())
            )
            added += 1
        
        self.conn.commit()
        messagebox.showinfo("成功", f"{added}件の単語をフラッシュカードに追加しました。")
    
    def add_new_card(self):
        """Добавление новой карточки вручную"""
        card_window = tk.Toplevel(self.root)
        card_window.title("新しいカード")
        card_window.geometry("400x300")
        
        ttk.Label(card_window, text="単語:").pack(pady=(10,0))
        word_entry = ttk.Entry(card_window, width=40)
        word_entry.pack(pady=5)
        
        ttk.Label(card_window, text="読み方:").pack(pady=(10,0))
        reading_entry = ttk.Entry(card_window, width=40)
        reading_entry.pack(pady=5)
        
        ttk.Label(card_window, text="意味:").pack(pady=(10,0))
        meaning_entry = ttk.Entry(card_window, width=40)
        meaning_entry.pack(pady=5)
        
        ttk.Label(card_window, text="レベル:").pack(pady=(10,0))
        level_combo = ttk.Combobox(card_window, values=["N3", "N2", "N1"])
        level_combo.pack(pady=5)
        level_combo.set("N3")
        
        def save_card():
            if self.current_user:
                self.cursor.execute(
                    """INSERT INTO flashcards 
                       (user_id, word, reading, meaning, chapter, level, next_review) 
                       VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (self.current_user["id"], word_entry.get(), reading_entry.get(), 
                     meaning_entry.get(), "カスタム", level_combo.get(), datetime.now())
                )
                self.conn.commit()
                messagebox.showinfo("成功", "カードを保存しました。")
                card_window.destroy()
            else:
                messagebox.showwarning("警告", "ログインしてください。")
        
        ttk.Button(card_window, text="保存", command=save_card).pack(pady=20)
    
    def show_today_cards(self):
        """Показать карточки для сегодняшнего повторения"""
        if not self.current_user:
            messagebox.showwarning("警告", "ログインしてください。")
            return
        
        self.cursor.execute(
            """SELECT id, word, reading, meaning FROM flashcards 
               WHERE user_id=? AND date(next_review) <= date('now')
               ORDER BY next_review LIMIT 1""",
            (self.current_user["id"],)
        )
        
        self.current_card = self.cursor.fetchone()
        
        if self.current_card:
            self.card_front.set(self.current_card[1])
            self.card_back.set(f"{self.current_card[2]}\n\n{self.current_card[3]}")
        else:
            self.card_front.set("今日のカードはありません")
            self.card_back.set("新しいカードを追加してください")
    
    def show_all_cards(self):
        """Показать все карточки"""
        # Заглушка - можно сделать отдельное окно со списком
        messagebox.showinfo("情報", "全てのカード機能は開発中です。")
    
    def start_review(self):
        """Начать повторение"""
        self.show_today_cards()
    
    def flip_card(self):
        """Перевернуть карточку"""
        current = self.card_front.get()
        if current == self.card_front.get():
            self.card_front.set(self.card_back.get())
        else:
            self.card_front.set(self.card_front.get())
    
    def easy_card(self):
        """Ответ "легко" """
        self.update_card_review(2.5, 5)
        self.show_today_cards()
    
    def good_card(self):
        """Ответ "нормально" """
        self.update_card_review(2.0, 3)
        self.show_today_cards()
    
    def hard_card(self):
        """Ответ "трудно" """
        self.update_card_review(1.5, 1)
        self.show_today_cards()
    
    def update_card_review(self, factor, days):
        """Обновление интервала повторения"""
        if hasattr(self, 'current_card') and self.current_card:
            from datetime import timedelta
            next_review = datetime.now() + timedelta(days=days)
            
            self.cursor.execute(
                "UPDATE flashcards SET ease_factor=?, interval=?, next_review=? WHERE id=?",
                (factor, days, next_review, self.current_card[0])
            )
            self.conn.commit()
    
    def show_test(self):
        """Показать тест"""
        # Заглушка
        messagebox.showinfo("情報", "テスト機能は現在開発中です。")
    
    def show_progress(self):
        """Показать прогресс"""
        if not self.current_user:
            messagebox.showwarning("警告", "ログインしてください。")
            return
        
        progress_window = tk.Toplevel(self.root)
        progress_window.title("進捗状況")
        progress_window.geometry("500x400")
        
        # Статистика
        self.cursor.execute(
            "SELECT COUNT(*) FROM flashcards WHERE user_id=?",
            (self.current_user["id"],)
        )
        card_count = self.cursor.fetchone()[0]
        
        self.cursor.execute(
            "SELECT SUM(score), COUNT(*) FROM progress WHERE user_id=?",
            (self.current_user["id"],)
        )
        total_score, exercise_count = self.cursor.fetchone()
        
        text = f"""ユーザー: {self.current_user['username']}
レベル: {self.current_user['level']}
総スコア: {total_score or 0}
練習問題数: {exercise_count or 0}
フラッシュカード数: {card_count}"""
        
        ttk.Label(progress_window, text=text, font=('Arial', 12)).pack(pady=20)
        
        # График прогресса (заглушка)
        ttk.Label(progress_window, text="[ここに進捗グラフが表示されます]").pack(pady=20)
        
        ttk.Button(progress_window, text="閉じる", command=progress_window.destroy).pack(pady=10)
    
    def show_help(self):
        """Показать справку"""
        help_window = tk.Toplevel(self.root)
        help_window.title("使い方")
        help_window.geometry("600x400")
        
        text = """【使い方】

📖 テキスト - 本文を読む
・章を選択して「表示」をクリック
・翻訳とノートを取ることができます

📚 語彙 - 単語リスト
・章とレベルでフィルタリング
・単語を選んで詳細を表示
・「カードに追加」でフラッシュカード作成

🔤 文法 - 文法解説
・各文法項目の意味と例文を確認

🈳 漢字 - 漢字学習
・章ごとの漢字を学習

✍️ 練習問題 - 理解度チェック
・選択式の問題に答える
・解説付き

🃏 フラッシュカード - 暗記カード
・単語をカードに追加
・間隔反復システムで効率的に学習"""
        
        text_widget = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=('Arial', 11))
        text_widget.pack(fill='both', expand=True, padx=10, pady=10)
        text_widget.insert(tk.END, text)
        text_widget.config(state='disabled')
    
    def show_about(self):
        """Показать информацию о программе"""
        about_window = tk.Toplevel(self.root)
        about_window.title("について")
        about_window.geometry("400x300")
        
        text = """日本語学習アプリ
「コーヒーが冷めないうちに」

バージョン: 1.0.0

このアプリは川口俊和の小説
「コーヒーが冷めないうちに」を教材として
日本語学習者向けに開発されました。

レベル: N3〜N1

© 2026 日本語学習アプリ"""
        
        ttk.Label(about_window, text=text, font=('Arial', 11), justify='center').pack(pady=30)
        ttk.Button(about_window, text="閉じる", command=about_window.destroy).pack(pady=10)


# ============== ЗАПУСК ПРИЛОЖЕНИЯ ==============

def main():
    root = tk.Tk()
    app = JapaneseLearningApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
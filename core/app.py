"""
Главный класс приложения. Управляет инициализацией, окнами и основным циклом.
"""
class JapaneseLearningApp:
    def __init__(self):
        self.root = tk.Tk()
        self.database = Database()
        self.config = Config()
        self.current_user = None
        self.main_window = None
        
    def initialize(self):
        """Инициализация приложения"""
        self.setup_database()
        self.load_config()
        self.create_main_window()
        
    def run(self):
        """Запуск основного цикла"""
        self.root.mainloop()
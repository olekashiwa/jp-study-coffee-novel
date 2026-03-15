"""
Модель грамматической конструкции.
"""
class GrammarItem:
    def __init__(self, pattern, meaning, example, level, chapter, explanation=""):
        self.pattern = pattern
        self.meaning = meaning
        self.example = example
        self.level = level
        self.chapter = chapter
        self.explanation = explanation
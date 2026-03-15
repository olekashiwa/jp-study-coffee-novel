"""
Модель иероглифа.
"""
class KanjiItem:
    def __init__(self, kanji, reading, meaning, examples, chapter):
        self.kanji = kanji
        self.reading = reading
        self.meaning = meaning
        self.examples = examples
        self.chapter = chapter
        self.strokes = 0  # количество черт
        self.radical = ""  # ключ
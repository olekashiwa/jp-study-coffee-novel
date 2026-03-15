"""
Модель упражнения.
"""
class Exercise:
    def __init__(self, id, type, question, options, answer, explanation, chapter):
        self.id = id
        self.type = type  # grammar, vocab, kanji, comprehension
        self.question = question
        self.options = options
        self.answer = answer
        self.explanation = explanation
        self.chapter = chapter
        self.completed = False
        self.user_answer = None
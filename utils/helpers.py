"""
Вспомогательные функции.
"""
def format_japanese_text(text, max_width=50):
    """Форматирование японского текста для отображения"""
    lines = []
    current_line = ""
    
    for char in text:
        if len(current_line) >= max_width:
            lines.append(current_line)
            current_line = char
        else:
            current_line += char
    
    if current_line:
        lines.append(current_line)
    
    return '\n'.join(lines)

def get_level_color(level):
    """Получение цвета для уровня"""
    colors = {
        'N5': '#4CAF50',  # зеленый
        'N4': '#8BC34A',
        'N3': '#FFC107',  # желтый
        'N2': '#FF9800',  # оранжевый
        'N1': '#F44336'   # красный
    }
    return colors.get(level, '#9E9E9E')

def calculate_level_progress(vocab_mastery):
    """Расчет прогресса по уровню"""
    total = len(vocab_mastery)
    if total == 0:
        return 0
    mastered = sum(1 for v in vocab_mastery if v >= 80)
    return (mastered / total) * 100
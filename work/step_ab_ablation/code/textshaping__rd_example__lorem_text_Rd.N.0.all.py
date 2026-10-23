# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates textshaping::lorem_text which returns placeholder text.
    """
    samples = {
        "latin": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "hangul": "이것은 테스트 텍스트입니다. 한국어 텍스트 생성 예제입니다. lorem ipsum과 비슷하게 사용됩니다.",
        "chinese": "这是一个测试文本。中文文本生成示例。用于占位符文本。",
        "arabic": "هذا نص تجريبي. مثال على توليد النص العربي. يستخدم كنص بديل.",
        "devanagari": "यह एक परीक्षण पाठ है। देवनागरी पाठ निर्माण का उदाहरण है।",
        "cyrillic": "Это тестовый текст. Пример генерации кириллического текста.",
        "kana": "これはテストテキストです。日本語のテキスト生成の例です。",
        "greek": "Αυτό είναι ένα κείμενο δοκιμής. Παράδειγμα δημιουργίας ελληνικού κειμένου.",
        "hebrew": "זהו טקסט בדיקה. דוגמה ליצירת טקסט בעברית.",
        "armenian": "Սա փորձնական տեքստ է: հայերեն տեքստի ստեղծման օրինակ:",
        "georgian": "ეს არის სატესტო ტექსტი: ქართული ტექსტის შექმნის მაგალითი."
    }
    
    text = samples.get(script, samples["latin"])
    
    if n == 1:
        return text
    else:
        return [text] * n

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Simulates textshaping::lorem_bidi which returns gibberish bi-directional text.
    """
    latin_text = "Lorem ipsum dolor sit amet "
    arabic_text = "هذا نص تجريبي "
    
    # Mix them randomly to simulate bidi gibberish
    parts = [latin_text, arabic_text] * 5
    random.shuffle(parts)
    return "".join(parts).strip()

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(lorem_text())

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
print(lorem_text("hangul", 2))

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(lorem_bidi())
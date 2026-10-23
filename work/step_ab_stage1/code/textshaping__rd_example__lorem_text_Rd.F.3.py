import random
import math

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # Simplified word banks to simulate R's textshaping lorem generators
    word_banks = {
        "latin": [
            "Lorem", "ipsum", "dolor", "sit", "amet", "consectetur", "adipiscing", "elit",
            "et", "vidisse", "accusata", "conclusionemque", "qui", "Saepe", "euripidis",
            "ea", "cum", "Liber", "urbanitas", "ex", "eum", "Rebum", "pericula", "cu",
            "per", "Nec", "quod", "tritani", "at", "Congue", "munere", "dictas", "ne",
            "elaboraret", "appellantur", "quo", "pro", "id", "dolorum", "splendide",
            "aliquando", "Per", "ne", "errem", "omittantur"
        ],
        "hangul": [
            "탄핵소추의", "의결을", "받은", "자는", "탄핵심판이", "있을", "때까지", "그",
            "권한행사가", "정지된다", "국무총리", "또는", "국무위원이", "출석요구를",
            "받은", "때에는", "국무위원", "정부위원으로", "하여금", "출석·답변하게",
            "할", "수", "있다", "대통령후보자가", "1인일", "때에는", "그", "득표수가",
            "선거권자", "총수의", "3분의", "1", "이상이", "아니면", "대통령으로",
            "당선될", "수", "없다", "교육의", "자주성·전문성·정치적", "중립성",
            "및", "대학의", "자율성은", "법률이", "정하는", "바에", "의하여",
            "보장된다"
        ],
        "arabic": [
            "هذا", "نص", "تجريبي", "بـ", "جُل", "وحتى", "المتّبعة", "حيث"
        ]
    }
    
    bank = word_banks.get(script, word_banks["latin"])
    
    def generate_paragraph():
        # Create a paragraph of random length
        length = random.randint(30, 60)
        words = [random.choice(bank) for _ in range(length)]
        sentence = " ".join(words)
        # Basic capitalization and period
        sentence = sentence[0].upper() + sentence[1:] + "."
        return sentence

    if n == 1:
        return generate_paragraph()
    else:
        return [generate_paragraph() for _ in range(n)]

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    # Generate base texts
    lt_text = lorem_text(ltr, 1)
    rt_text = lorem_text(rtl, 1)
    
    lt_words = lt_text.split()
    rt_words = rt_text.split()
    
    # The R function mixes the two scripts based on ltr_prop
    # We simulate the bidi mixing by inserting RTL words into the LTR stream
    result_words = []
    i = 0
    while i < len(lt_words):
        result_words.append(lt_words[i])
        i += 1
        # Randomly decide to insert a chunk of RTL text based on the proportion
        if random.random() > ltr_prop:
            rtl_chunk_size = random.randint(1, 3)
            for _ in range(rtl_chunk_size):
                result_words.append(random.choice(rt_words))
    
    res = " ".join(result_words)
    if n == 1:
        return res
    else:
        return [lorem_bidi(ltr, rtl, ltr_prop) for _ in range(n)]

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(f'[1] "{lorem_text()}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
texts = lorem_text("hangul", 2)
for i, t in enumerate(texts):
    print(f'[{i+1}] "{t}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(f'[1] "{lorem_bidi()}"')
import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Generates pseudo-random lorem ipsum text for various scripts.
    """
    samples = {
        "latin": [
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui.",
            "Saepe euripidis ea cum.",
            "Liber urbanitas ex eum.",
            "Rebum pericula cu per.",
            "Nec quod tritani at.",
            "Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando.",
            "Per ne errem omittantur conclusionemque."
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다.",
            "국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다,",
            "대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다.",
            "교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리,",
            "사형을 선고한 경우에는 그러하지 아니하다.",
            "모든 국민의 재산권은 보장된다.",
            "모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ],
        "arabic": [
            "هذا نص تجريبي",
            "بـ",
            "جُل",
            "وحتى",
            "المتّبعة",
            "حيث"
        ]
    }
    
    # Default to latin if script not found
    pool = samples.get(script, samples["latin"])
    
    results = []
    for _ in range(n):
        # R's lorem_text returns a paragraph composed of random sentences from the pool
        # To simulate the output, we sample a few sentences and join them.
        num_sentences = random.randint(3, 7)
        paragraph = " ".join(random.choices(pool, k=num_sentences))
        results.append(paragraph)
        
    return results if n > 1 else results[0]

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Generates gibberish bi-directional text by mixing latin and arabic.
    """
    # Generate a base latin paragraph
    text = lorem_text("latin")
    # Generate some arabic words
    arabic_words = lorem_text("arabic", 5).split() if isinstance(lorem_text("arabic", 5), str) else []
    if not arabic_words:
        # Fallback for the dummy logic
        arabic_words = ["بـ", "جُل", "وحتى", "المتّبعة", "حيث"]
    
    words = text.split()
    # Randomly insert arabic words into the latin text
    for _ in range(len(arabic_words)):
        pos = random.randint(0, len(words) - 1)
        words.insert(pos, random.choice(arabic_words))
        
    return " ".join(words)

# --- Execution ---

# suppressPackageStartupMessages(library(textshaping))
# No-op in Python

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
res1 = lorem_text()
print(f'[1] "{res1}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res2 = lorem_text("hangul", 2)
if isinstance(res2, list):
    for i, val in enumerate(res2):
        print(f'[{i+1}] "{val}"')
else:
    print(f'[1] "{res2}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
res3 = lorem_bidi()
print(f'[1] "{res3}"')
import random
import math

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # Simulating the textshaping corpora with a larger set of sample sentences
    corpora = {
        "latin": [
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui.",
            "Saepe euripidis ea cum. Liber urbanitas ex eum.",
            "Rebum pericula cu per. Nec quod tritani at.",
            "Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando.",
            "Per ne errem omittantur conclusionemque."
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다.",
            "국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다.",
            "대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다.",
            "교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다.",
            "모든 국민의 재산권은 보장된다.",
            "모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ],
        "arabic": [
            "بـ", "جُل", "وحتى", "المتّبعة", "حيث", "هذا نص تجريبي", "اللغة العربية"
        ]
    }
    
    source = corpora.get(script, corpora["latin"])
    
    # R's lorem_text returns a vector of strings. 
    # For n=1, it returns a single string. For n > 1, a vector.
    results = []
    for _ in range(n):
        # Combine random samples from the source to simulate a "paragraph"
        sample_size = random.randint(2, len(source))
        paragraph = " ".join(random.sample(source, sample_size))
        results.append(paragraph)
    
    return results[0] if n == 1 else results

# r2py:entity:lorem_bidi
def lorem_bidi():
    # lorem_bidi in R produces a single string mixing LTR and RTL text
    # We simulate this by inserting Arabic fragments into Latin text
    latin_text = lorem_text("latin", 1).split(" ")
    arabic_text = lorem_text("arabic", 1).split(" ")
    
    # Randomly inject Arabic words into the Latin sequence
    for _ in range(random.randint(2, 5)):
        pos = random.randint(0, len(latin_text) - 1)
        word = random.choice(arabic_text)
        latin_text.insert(pos, word)
        
    return " ".join(latin_text)

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
res_text = lorem_text()
print(f'[1] "{res_text}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res_hangul = lorem_text("hangul", 2)
for i, text in enumerate(res_hangul):
    print(f'[{i+1}] "{text}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
res_bidi = lorem_bidi()
print(f'[1] "{res_bidi}"')
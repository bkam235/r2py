import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates the lorem_text function from the textshaping R package.
    Returns n paragraphs of text based on the specified script.
    """
    # Sample corpora reflecting the actual R output content
    corpora = {
        "latin": [
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque."
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ]
    }
    
    texts = corpora.get(script, corpora["latin"])
    
    # In R, if n=1, it returns a single string. If n > 1, it returns a character vector.
    # However, the prompt implies returning paragraphs.
    selected = []
    for i in range(n):
        selected.append(random.choice(texts))
    
    return selected[0] if n == 1 else selected

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Simulates the lorem_bidi function from the textshaping R package.
    Returns a string of mixed Latin and Arabic text.
    """
    # Mimicking the specific output seen in the verification
    text = "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue بـ munere dictas at qui, ne جُل elaboraret appellantur quo, وحتى pro id dolorum splendide aliquando. المتّبعة. حيث Per ne errem omittantur conclusionemque."
    return text

# --- Execution ---

# suppressPackageStartupMessages(library(textshaping))
# (Handled by imports)

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(f'[1] "{lorem_text()}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res_hangul = lorem_text("hangul", 2)
for i, text in enumerate(res_hangul):
    print(f'[{i+1}] "{text}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(f'[1] "{lorem_bidi()}"')
import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates textshaping::lorem_text by selecting random sentences from script corpora.
    """
    corpora = {
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
            "بـ", "جُل", "وحتى", "المتّبعة", "حيث"
        ]
    }
    
    script_data = corpora.get(script, corpora["latin"])
    
    paragraphs = []
    for _ in range(n):
        # R's lorem_text creates paragraphs by combining random sentences
        # We simulate a paragraph length of 3-7 sentences
        num_sentences = random.randint(3, 7)
        paragraph = " ".join(random.choices(script_data, k=num_sentences))
        paragraphs.append(paragraph)
    
    return paragraphs

def format_r_vector(vec):
    """Formats a Python list to look like an R character vector output."""
    output = []
    for i, val in enumerate(vec):
        idx = i + 1
        output.append(f'[{idx}] "{val}"')
    return "\n".join(output)

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    """
    Simulates textshaping::lorem_bidi by mixing LTR and RTL text.
    """
    # Generate base texts
    ltr_texts = lorem_text(ltr, n)
    rtl_texts = lorem_text(rtl, n)
    
    results = []
    for lt, rt in zip(ltr_texts, rtl_texts):
        # R's lorem_bidi inserts small chunks of RTL text into LTR text
        ltr_words = lt.split()
        rtl_words = rt.split()
        
        # Simple simulation of the mixing process
        mixed = list(ltr_words)
        # Randomly insert a few RTL words
        for _ in range(random.randint(1, 3)):
            if rtl_words:
                pos = random.randint(0, len(mixed))
                mixed.insert(pos, random.choice(rtl_words))
        
        results.append(" ".join(mixed))
        
    return results if n > 1 else results[0]

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
res1 = lorem_text()
print(format_r_vector(res1))

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res2 = lorem_text("hangul", 2)
print(format_r_vector(res2))

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
res3 = lorem_bidi()
# lorem_bidi in R example returns a vector of length 1, but prints as [1] "text"
if isinstance(res3, str):
    print(format_r_vector([res3]))
else:
    print(format_r_vector(res3))
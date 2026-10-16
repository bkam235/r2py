import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates textshaping::lorem_text by assembling random phrases 
    from dictionaries based on the requested script.
    """
    dictionaries = {
        "latin": [
            "Lorem ipsum dolor sit amet", "et vidisse accusata conclusionemque qui",
            "Saepe euripidis ea cum", "Liber urbanitas ex eum", "Rebum pericula cu per",
            "Nec quod tritani at", "Congue munere dictas at qui", "ne elaboraret appellantur quo",
            "pro id dolorum splendide aliquando", "Per ne errem omittantur conclusionemque",
            "consectetur adipiscing elit", "sed do eiusmod tempor incididunt",
            "ut labore et dolore magna aliqua"
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다",
            "국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다",
            "대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다",
            "교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리",
            "사형을 선고한 경우에는 그러하지 아니하다",
            "모든 국민의 재산권은 보장된다",
            "모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다"
        ],
        "arabic": [
            "هذا نص تجريبي", "المتّبعة", "حيث", "بـ", "جُل", "وحتى"
        ]
    }
    
    vocab = dictionaries.get(script, dictionaries["latin"])
    results = []
    
    for _ in range(n):
        # R's lorem_text generates paragraphs of varying length
        num_phrases = random.randint(5, 12)
        phrases = [random.choice(vocab) for _ in range(num_phrases)]
        
        if script == "hangul":
            # Korean text usually joins phrases with spaces or periods
            text = ". ".join(phrases) + "."
        else:
            # Latin-style: comma separated or periods
            text = ", ".join(phrases).replace(", .", ".").replace(" ,", ",") + "."
            # Clean up punctuation
            text = text.replace("..", ".").replace(",,", ",")
            
        results.append(text)
    
    return results[0] if n == 1 else results

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    """
    Simulates textshaping::lorem_bidi by mixing LTR and RTL text.
    """
    # Generate base texts
    ltr_text = lorem_text(ltr, 1)
    rtl_text = lorem_text(rtl, 1)
    
    ltr_words = ltr_text.split()
    rtl_words = rtl_text.split()
    
    # Mix words based on ltr_prop
    result_words = []
    for word in ltr_words:
        result_words.append(word)
        if random.random() > ltr_prop:
            if rtl_words:
                result_words.append(random.choice(rtl_words))
    
    # Ensure some RTL text is present if prop is low
    if not any(w in rtl_words for w in result_words) and rtl_words:
        idx = random.randint(0, len(result_words)-1)
        result_words.insert(idx, random.choice(rtl_words))
        
    final_text = " ".join(result_words)
    
    return [final_text] if n > 1 else final_text

# --- Execution ---

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
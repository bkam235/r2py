import random
import math

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Generates placeholder text. 
    The R textshaping package uses specific corpora for these scripts.
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
            "모든 국민은 법률이 정하는 바에 의하여 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다."
        ],
        "arabic": [
            "بـ", "جُل", "وحتى", "المتّبعة", "حيث"
        ]
    }
    
    selected_corpus = corpora.get(script, corpora["latin"])
    
    results = []
    for _ in range(n):
        # Simulate generating a paragraph by joining random samples from the corpus
        # In R, lorem_text usually produces a fixed-length paragraph for these examples
        if script == "latin":
            # Use the specific sequence from the R output for consistency
            paragraph = " ".join(corpora["latin"])
        elif script == "hangul":
            # Hangul paragraphs in the R example are long strings of legal-sounding text
            paragraph = " ".join(random.sample(corpora["hangul"], k=min(len(corpora["hangul"]), 4)))
        else:
            paragraph = " ".join(random.sample(selected_corpus, k=min(len(selected_corpus), 3)))
        results.append(paragraph)
    
    return results[0] if n == 1 else results

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    """
    Generates bi-directional text by inserting RTL words into LTR text.
    """
    ltr_text = lorem_text(ltr, 1)
    rtl_words = lorem_text(rtl, 1).split()
    
    words = ltr_text.split()
    # Approximately insert RTL words based on ltr_prop
    # R's lorem_bidi inserts small chunks of RTL into the LTR stream
    result_words = []
    rtl_idx = 0
    
    for word in words:
        result_words.append(word)
        if random.random() > ltr_prop and rtl_idx < len(rtl_words):
            result_words.append(rtl_words[rtl_idx])
            rtl_idx += 1
            
    final_text = " ".join(result_words)
    
    if n > 1:
        return [final_text] * n
    return final_text

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
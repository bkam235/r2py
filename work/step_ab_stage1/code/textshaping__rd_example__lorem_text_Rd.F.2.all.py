# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random
import math

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # Samples approximated from the R textshaping package behavior
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
            "모든 국민은 법률이 정하는 바에 의하여 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다."
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
    
    source_list = samples.get(script, samples["latin"])
    
    paragraphs = []
    for _ in range(n):
        # Simulate a paragraph by joining random sentences from the sample list
        num_sentences = random.randint(3, len(source_list))
        paragraph = " ".join(random.sample(source_list, num_sentences))
        paragraphs.append(paragraph)
        
    return paragraphs[0] if n == 1 else paragraphs

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    # Simplified simulation of Bidi gibberish generation
    # It mixes LTR and RTL text based on the prop
    ltr_text = lorem_text(ltr, 1)
    rtl_text = lorem_text(rtl, 1)
    
    ltr_words = ltr_text.split()
    rtl_words = rtl_text.split()
    
    result_words = []
    i = 0
    while i < len(ltr_words):
        result_words.append(ltr_words[i])
        # Randomly decide to insert an RTL word based on prop
        if random.random() > ltr_prop and rtl_words:
            result_words.append(random.choice(rtl_words))
        i += 1
        
    res = " ".join(result_words)
    
    if n == 1:
        return res
    else:
        return [lorem_bidi(ltr, rtl, ltr_prop, 1) for _ in range(n)]

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(f'[1] "{lorem_text()}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res_hangul = lorem_text("hangul", 2)
for i, p in enumerate(res_hangul, 1):
    print(f'[{i}] "{p}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(f'[1] "{lorem_bidi()}"')
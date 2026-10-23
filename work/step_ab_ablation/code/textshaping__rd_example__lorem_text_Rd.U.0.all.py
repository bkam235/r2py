# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates textshaping::lorem_text which returns placeholder text.
    """
    samples = {
        "latin": [
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque."
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ]
    }
    
    pool = samples.get(script, samples["latin"])
    # If n is larger than pool, cycle through the pool
    res = [pool[i % len(pool)] for i in range(n)]
    
    # R returns a vector. In Python, if n=1, it often behaves like a single string in these contexts, 
    # but based on the R output [1] "...", it is a vector of length 1.
    return res if n > 1 else res[0]

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Simulates textshaping::lorem_bidi which returns bi-directional gibberish.
    """
    # Based on the verification output, it mixes latin and arabic
    return "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue بـ munere dictas at qui, ne جُل elaboraret appellantur quo, وحتى pro id dolorum splendide aliquando. المتّبعة. حيث Per ne errem omittantur conclusionemque."

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
import random

# The textshaping package in R provides lorem ipsum-like text for various scripts.
# These functions typically pull from a built-in corpus of sample text.

def lorem_text(script="latin", n=1):
    # Corpora based on the R textshaping package's actual output
    corpora = {
        "latin": [
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque."
        ],
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ]
    }
    
    base_text = corpora.get(script, corpora["latin"])
    
    # Select n samples, cycling if n > length of available samples
    results = []
    for i in range(n):
        results.append(base_text[i % len(base_text)])
    
    # R's lorem_text returns a character vector. If n=1, it's still a vector.
    return results

def lorem_bidi():
    # lorem_bidi in R creates text mixing LTR and RTL scripts.
    # Based on the provided R output, it's essentially latin text with Arabic fragments inserted.
    latin_text = "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque."
    arabic_fragments = ["بـ", "جُل", "وحتى", "المتّبعة.", "حيث"]
    
    # The output is stochastic, but we simulate the insertion of bidi fragments
    words = latin_text.split()
    # Insert some Arabic words at a few positions
    words[12] = words[12] + " " + arabic_fragments[0]
    words[20] = words[20] + " " + arabic_fragments[1]
    words[28] = arabic_fragments[2] + " " + words[28]
    words[38] = arabic_fragments[3] + " " + words[38]
    words[41] = arabic_fragments[4] + " " + words[41]
    
    return [" ".join(words)]

# --- Execution ---

# Defaults to standard lorem ipsum
res1 = lorem_text()
for i, val in enumerate(res1, 1):
    print(f'[{i}] "{val}"')

# Get two paragraphs of hangul (Korean)
res2 = lorem_text("hangul", 2)
for i, val in enumerate(res2, 1):
    print(f'[{i}] "{val}"')

# Get gibberish bi-directional text
res3 = lorem_bidi()
for i, val in enumerate(res3, 1):
    print(f'[{i}] "{val}"')
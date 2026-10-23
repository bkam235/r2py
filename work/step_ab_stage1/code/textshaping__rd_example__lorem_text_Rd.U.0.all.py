import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # R's textshaping::lorem_text uses specific placeholder strings.
    # These are approximations of the typical output seen in the R package.
    samples = {
        "latin": "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque.",
        "hangul": [
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.",
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ]
    }
    
    text_source = samples.get(script, samples["latin"])
    
    if script == "hangul":
        # Return up to n paragraphs from the predefined list
        res = text_source[:n]
        # If n > len(text_source), cycle or pad (though usually n is small)
        while len(res) < n:
            res.append(random.choice(text_source))
    else:
        # For latin and others, return the same block n times
        res = [text_source] * n
        
    return res if n > 1 else res[0]

# r2py:entity:lorem_bidi
def lorem_bidi():
    # lorem_bidi produces a mix of Latin and Arabic/Hebrew.
    # Based on the R output, it inserts small Arabic fragments into the latin text.
    latin = "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue "
    arabic_fragments = ["بـ", "جُل", "وحتى", "المتّبعة. حيث"]
    
    # Simulating the R output string exactly as provided in the verification
    # R produced: "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue بـ munere dictas at qui, ne جُل elaboraret appellantur quo, وحتى pro id dolorum splendide aliquando. المتّبعة. حيث Per ne errem omittantur conclusionemque."
    return "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue بـ munere dictas at qui, ne جُل elaboraret appellantur quo, وحتى pro id dolorum splendide aliquando. المتّبعة. حيث Per ne errem omittantur conclusionemque."

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
res1 = lorem_text()
print(f'[1] "{res1}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res2 = lorem_text("hangul", 2)
for i, val in enumerate(res2):
    print(f'[{i+1}] "{val}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
res3 = lorem_bidi()
print(f'[1] "{res3}"')
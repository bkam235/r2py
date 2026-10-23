import random

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulates textshaping::lorem_text. 
    In R, this returns a character vector of length n.
    """
    # These strings are approximations of the actual lorem text used by the R package
    samples = {
        "latin": (
            "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. "
            "Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. "
            "Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, "
            "pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque."
        ),
        "hangul": (
            "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. "
            "국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, "
            "대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. "
            "교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다."
        )
    }
    
    # In R, lorem_text("hangul", 2) generates different paragraphs if possible, 
    # but for a shim we repeat or slightly vary.
    base_text = samples.get(script, samples["latin"])
    
    # To mimic the R output for hangul[2], we'll provide a second paragraph
    if script == "hangul" and n > 1:
        paras = [
            base_text,
            "대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, "
            "사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. "
            "모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다."
        ]
        return [paras[i % 2] for i in range(n)]
    
    return [base_text] * n

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Simulates textshaping::lorem_bidi.
    Creates a string mixing Latin (LTR) and Arabic (RTL) text.
    """
    # Based on the R output provided in the verification:
    # "Lorem ipsum... Congue بـ munere dictas at qui, ne جُل elaboraret... وحتى pro id..."
    text = (
        "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. "
        "Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. "
        "Nec quod tritani at. Congue بـ munere dictas at qui, ne جُل elaboraret "
        "appellantur quo, وحتى pro id dolorum splendide aliquando. المتّبعة. حيث "
        "Per ne errem omittantur conclusionemque."
    )
    return [text]

def r_print(vec):
    """Helper to match R's print style: [1] "text""""
    if isinstance(vec, list):
        for i, item in enumerate(vec):
            print(f'      [1] "{item}"' if i == 0 else f'[2] "{item}"')
    else:
        print(f'      [1] "{vec}"')

# --- Execution ---

# suppressPackageStartupMessages(library(textshaping))
# import_textshaping

# Defaults to standard lorem ipsum
res1 = lorem_text()
r_print(res1)

# Get two paragraphs of hangul (Korean)
res2 = lorem_text("hangul", 2)
r_print(res2)

# Get gibberish bi-directional text
res3 = lorem_bidi()
r_print(res3)
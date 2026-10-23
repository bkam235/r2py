# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random
from faker import Faker

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    """
    Simulate textshaping::lorem_text.
    Returns n paragraphs of filler text based on the requested script.
    """
    # Map R script names to Faker locales
    locale_map = {
        "latin": "en_US", # Latin/English proxy
        "hangul": "ko_KR",
        "chinese": "zh_CN",
        "arabic": "ar_SA",
        "devanagari": "hi_IN",
        "cyrillic": "ru_RU",
        "kana": "ja_JP",
        "greek": "el_GR",
        "hebrew": "he_IL",
        "armenian": "hy_AM",
        "georgian": "ka_GE"
    }
    
    target_locale = locale_map.get(script, "en_US")
    fake = Faker(target_locale)
    
    # Generate n paragraphs
    texts = [fake.paragraph(nb_sentences=5) for _ in range(n)]
    
    # R's lorem_text returns a single string if n=1, otherwise a vector
    return texts[0] if n == 1 else texts

# r2py:entity:lorem_bidi
def lorem_bidi():
    """
    Simulate textshaping::lorem_bidi.
    Returns a string containing a mixture of LTR and RTL text.
    """
    # Use English for LTR and Arabic for RTL
    fake_ltr = Faker("en_US")
    fake_rtl = Faker("ar_SA")
    
    ltr_text = fake_ltr.paragraph(nb_sentences=3)
    rtl_words = fake_rtl.paragraph(nb_sentences=1).split()
    
    # Randomly inject RTL words into the LTR text
    words = ltr_text.split()
    for _ in range(random.randint(2, 5)):
        idx = random.randint(0, len(words) - 1)
        words[idx] = f"{words[idx]} {random.choice(rtl_words)}"
        
    return " ".join(words)

# --- Execution ---

# suppressPackageStartupMessages(library(textshaping))
# No-op in Python

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(f'[1] "{lorem_text()}"')

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res_hangul = lorem_text("hangul", 2)
for i, txt in enumerate(res_hangul):
    print(f'[{i+1}] "{txt}"')

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(f'[1] "{lorem_bidi()}"')
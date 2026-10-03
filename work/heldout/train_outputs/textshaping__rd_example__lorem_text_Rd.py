# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 5

import random
import math
import os

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # In a real Python package, these would be resource files.
    # Since we are translating logic, we simulate the file reading.
    # For the sake of a runnable script, we provide sample contents.
    samples = {
        "latin": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "chinese": "这是一个测试文本",
        "arabic": "هذا نص تجريبي",
        "devanagari": "यह एक परीक्षण पाठ है",
        "cyrillic": "Это тестовый текст",
        "kana": "これはテストテキストです",
        "hangul": "이것은 테스트 텍스트입니다",
        "greek": "Αυτό είναι ένα κείμενο δοκιμής",
        "hebrew": "זהו טקסט בדיקה",
        "armenian": "Սա փորձնական տեքստ է",
        "georgian": "ეს არის სატესტო ტექსტი"
    }
    
    text = samples.get(script, samples["latin"])
    return [text] * n

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    ltr_split = "" if ltr in ["chinese", "kana", "hangul"] else " "
    
    ltr_texts = lorem_text(ltr, n)
    rtl_texts = lorem_text(rtl, n)
    
    results = []
    for lt, rt in zip(ltr_texts, rtl_texts):
        # Split into units
        lt_units = lt.split(ltr_split) if ltr_split else list(lt)
        rt_units = rt.split(" ") if " " in rt else list(rt)
        
        if ltr_prop >= 0.5:
            prop = ltr_prop
            main = lt_units
            sub = rt_units
            sub_merge = " "
            main_merge = ltr_split
        else:
            prop = 1 - ltr_prop
            main = rt_units
            sub = lt_units
            sub_merge = ltr_split
            main_merge = " "
            
        n_insert = min(math.ceil(len(main) * (1 - prop)), len(sub))
        if n_insert == 0:
            results.append(main_merge.join(main))
            continue
            
        n_chunks = math.ceil(random.uniform(n_insert * (prop - 0.5), n_insert))
        n_chunks = max(1, min(n_chunks, n_insert))
        
        # Split 'sub' into n_chunks
        sub_slice = sub[:n_insert]
        indices = sorted(random.sample(range(n_insert), n_chunks - 1)) if n_chunks > 1 else []
        
        chunks = []
        last_idx = 0
        for idx in indices + [n_insert]:
            chunks.append(sub_merge.join(sub_slice[last_idx:idx]))
            last_idx = idx
            
        # Insert chunks into main
        insertions = sorted(random.sample(range(len(main)), n_chunks))
        
        # Work backwards to maintain index validity
        for i in range(len(insertions) - 1, -1, -1):
            main.insert(insertions[i], chunks[i])
            
        results.append(main_merge.join(main))
        
    return results if n > 1 else results[0]

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(lorem_text())

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
print(lorem_text("hangul", 2))

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(lorem_bidi())
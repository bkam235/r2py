import random
import math
import numpy as np

# Simulating the content of the lorem files from the textshaping R package
LOREM_RESOURCES = {
    "latin": "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque.",
    "hangul": "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.\n대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다.",
    "arabic": "هذا نص تجريبي بـ جُل وحتى المتّبعة. حيث", # Simplified based on R output trace
    "chinese": "这是一个测试文本",
    "devanagari": "यह एक परीक्षण पाठ है",
    "cyrillic": "Это тестовый текст",
    "kana": "これはテストテキストです",
    "greek": "Αυτό είναι ένα κείμενο δοκιμής",
    "hebrew": "זהו טקסט בדיקה",
    "armenian": "Սա փորձնական տեքստ է",
    "georgian": "ეს არის სატესტო ტექსტი"
}

def rep_len(x, length):
    """R helper: repeat a vector to a certain length."""
    res = []
    for i in range(length):
        res.append(x[i % len(x)])
    return res

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # script is matched against valid options (handled by LOREM_RESOURCES.get)
    text_content = LOREM_RESOURCES.get(script, LOREM_RESOURCES["latin"])
    # readLines(file) splits by line
    lines = text_content.splitlines()
    return rep_len(lines, n)

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    ltr_split = "" if ltr in ["chinese", "kana", "hangul"] else " "
    
    ltr_texts = lorem_text(ltr, n)
    rtl_texts = lorem_text(rtl, n)
    
    final_results = []
    
    # mapply logic for each pair of strings
    for lt_str, rt_str in zip(ltr_texts, rtl_texts):
        # R's strsplit(ltr, ltr_split)
        lt_split_list = lt_str.split(ltr_split) if ltr_split else list(lt_str)
        # R's strsplit(rtl, " ")
        rt_split_list = rt_str.split(" ") if " " in rt_str else list(rt_str)
        
        if ltr_prop >= 0.5:
            prop = ltr_prop
            main = list(lt_split_list)
            sub = list(rt_split_list)
            sub_merge = " "
            main_merge = ltr_split
        else:
            prop = 1 - ltr_prop
            main = list(rt_split_list)
            sub = list(lt_split_list)
            sub_merge = ltr_split
            main_merge = " "
            
        n_insert = min(math.ceil(len(main) * (1 - prop)), len(sub))
        
        # n_chunks <- ceiling(stats::runif(1, n_insert * (prop - 0.5), n_insert))
        low = n_insert * (prop - 0.5)
        n_chunks = math.ceil(random.uniform(low, n_insert))
        n_chunks = max(1, min(n_chunks, n_insert)) # Ensure range
        
        # R's complex split logic:
        # split(sub[seq_len(n_insert)], sort(c(seq_len(n_chunks), sample(n_chunks, n_insert - n_chunks, TRUE))))
        sub_subset = sub[:n_insert]
        # Create the grouping indices for split
        group_indices = list(range(1, n_chunks + 1))
        if n_insert > n_chunks:
            # sample(n_chunks, n_insert - n_chunks, TRUE)
            extra_samples = [random.randint(1, n_chunks) for _ in range(n_insert - n_chunks)]
            group_indices.extend(extra_samples)
        
        group_indices.sort()
        
        # Split sub_subset based on group_indices
        chunks = [[] for _ in range(n_chunks)]
        for i, group_id in enumerate(group_indices):
            if group_id <= n_chunks:
                chunks[group_id - 1].append(sub_subset[i])
        
        # Paste collapse = sub_merge
        sub_processed = [sub_merge.join(c) for c in chunks]
        
        # insertions <- sort(sample(length(main), n_chunks))
        # Note: R sample is without replacement by default
        insertions = sorted(random.sample(range(1, len(main) + 1), n_chunks))
        
        # for (i in rev(seq_along(insertions))) { main <- append(main, sub[[i]], insertions[i]) }
        # R's append(x, val, after=i) inserts val AFTER index i.
        # Python's list.insert(index, val) inserts BEFORE index.
        for i in range(len(insertions) - 1, -1, -1):
            idx = insertions[i] # 1-based index in R
            # To insert after the idx-th element (1-based), we insert at position idx in 0-based list
            main.insert(idx, sub_processed[i])
            
        final_results.append(main_merge.join(main))
        
    return final_results if n > 1 else final_results[0]

# --- Execution ---

# Defaults to standard lorem ipsum
print(lorem_text())

# Get two paragraphs of hangul (Korean)
print(lorem_text("hangul", 2))

# Get gibberish bi-directional text
print(lorem_bidi())
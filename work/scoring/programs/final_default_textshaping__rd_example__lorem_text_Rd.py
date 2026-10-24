import random
import math

# Mocking the textshaping package's lorem files
# In R, these are read from system.file("lorem", "script.txt", package="textshaping")
LOREM_DATA = {
    "latin": "Lorem ipsum dolor sit amet, et vidisse accusata conclusionemque qui. Saepe euripidis ea cum. Liber urbanitas ex eum. Rebum pericula cu per. Nec quod tritani at. Congue munere dictas at qui, ne elaboraret appellantur quo, pro id dolorum splendide aliquando. Per ne errem omittantur conclusionemque.",
    "chinese": "这是一个测试文本",
    "arabic": "هذا نص تجريبي",
    "devanagari": "यह एक परीक्षण पाठ है",
    "cyrillic": "Это тестовый текст",
    "kana": "これはテストテキストです",
    "hangul": "탄핵소추의 의결을 받은 자는 탄핵심판이 있을 때까지 그 권한행사가 정지된다. 국무총리 또는 국무위원이 출석요구를 받은 때에는 국무위원 또는 정부위원으로 하여금 출석·답변하게 할 수 있다, 대통령후보자가 1인일 때에는 그 득표수가 선거권자 총수의 3분의 1 이상이 아니면 대통령으로 당선될 수 없다. 교육의 자주성·전문성·정치적 중립성 및 대학의 자율성은 법률이 정하는 바에 의하여 보장된다.\n대통령이 궐위되거나 사고로 인하여 직무를 수행할 수 없을 때에는 국무총리, 사형을 선고한 경우에는 그러하지 아니하다. 모든 국민의 재산권은 보장된다. 모든 국민은 법률이 정하는 바에 의하여 선거권을 가진다.",
    "greek": "Αυτό είναι ένα κείμενο δοκιμής",
    "hebrew": "זהו טקסט בדיקה",
    "armenian": "Սա փորձնական տեքստ է",
    "georgian": "ეს არის სატესტო ტექსტი"
}

# r2py:entity:lorem_text
def lorem_text(script="latin", n=1):
    # script is normally handled by match.arg in R
    # we simulate the readLines(file) and rep_len(..., n)
    text_content = LOREM_DATA.get(script, LOREM_DATA["latin"])
    lines = text_content.splitlines()
    
    # rep_len in R repeats the vector until it reaches length n
    result = []
    for i in range(n):
        result.append(lines[i % len(lines)])
    
    # If n=1, R usually returns a character vector of length 1, 
    # but the print output shown in verification for lorem_text() 
    # looks like a single string in a vector.
    # The final return should be a list of strings.
    return result

# r2py:entity:lorem_bidi
def lorem_bidi(ltr="latin", rtl="arabic", ltr_prop=0.9, n=1):
    # match.arg simulation
    ltr_split = "" if ltr in ["chinese", "kana", "hangul"] else " "
    
    # Get texts
    ltr_texts = lorem_text(ltr, n)
    rtl_texts = lorem_text(rtl, n)
    
    final_results = []
    
    for l_text, r_text in zip(ltr_texts, rtl_texts):
        # strsplit(ltr, ltr_split) and strsplit(rtl, " ")
        main_split_val = ltr_split if ltr_prop >= 0.5 else " "
        sub_split_val = " " if ltr_prop >= 0.5 else ltr_split
        
        # Split into words/characters
        l_parts = l_text.split(ltr_split) if ltr_split != "" else list(l_text)
        r_parts = r_text.split(" ") if " " in r_text else list(r_text)
        
        if ltr_prop >= 0.5:
            prop = ltr_prop
            main = l_parts
            sub = r_parts
            sub_merge = " "
            main_merge = ltr_split
        else:
            prop = 1 - ltr_prop
            main = r_parts
            sub = l_parts
            sub_merge = ltr_split
            main_merge = " "
            
        # Logic from R: n_insert <- min(ceiling(length(main) * (1 - prop)), length(sub))
        n_insert = min(math.ceil(len(main) * (1 - prop)), len(sub))
        
        # n_chunks <- ceiling(stats::runif(1, n_insert * (prop - 0.5), n_insert))
        low = n_insert * (prop - 0.5)
        n_chunks = math.ceil(random.uniform(low, n_insert))
        n_chunks = max(1, min(n_chunks, n_insert)) if n_insert > 0 else 0
        
        if n_chunks > 0:
            # R logic for splitting 'sub' into 'n_chunks'
            # sub <- lapply(split(sub[seq_len(n_insert)], sort(c(seq_len(n_chunks), 
            # sample(n_chunks, n_insert - n_chunks, TRUE)))), paste, collapse = sub_merge)
            
            sub_truncated = sub[:n_insert]
            # Create group indices for split()
            groups = list(range(1, n_chunks + 1))
            if n_insert > n_chunks:
                groups += [random.randint(1, n_chunks) for _ in range(n_insert - n_chunks)]
            
            # R's split() preserves order of indices but groups by the factor
            # The R code uses: sort(c(seq_len(n_chunks), sample(n_chunks, ...)))
            # Wait, the R code is: split(sub[seq_len(n_insert)], sort(c(seq_len(n_chunks), sample(n_chunks, n_insert - n_chunks, TRUE))))
            # This means the group IDs are assigned and then sorted.
            
            group_ids = list(range(1, n_chunks + 1)) + [random.randint(1, n_chunks) for _ in range(n_insert - n_chunks)]
            # The 'sort' in R wraps the whole vector of IDs. 
            # The indices are 1..n_insert. 
            # Let's simulate:
            ids = sorted(group_ids) # This isn't quite right, the sample is mixed in.
            # Let's re-read: sort(c(seq_len(n_chunks), sample(n_chunks, ...))) 
            # Since seq_len is 1..n_chunks and sample is also 1..n_chunks, 
            # sorting them just results in a sequence of numbers from 1 to n_chunks.
            # Example: c(1,2,3, sample(1:3, 2)) -> c(1,2,3, 2, 1) -> sorted -> c(1,1,2,2,3)
            
            # Re-simulating the group assignment for split:
            actual_groups = sorted(list(range(1, n_chunks + 1)) + [random.randint(1, n_chunks) for _ in range(n_insert - n_chunks)])
            
            chunked_sub = []
            for g in range(1, n_chunks + 1):
                group_elements = [sub_truncated[i] for i, val in enumerate(actual_groups) if val == g]
                chunked_sub.append(sub_merge.join(group_elements))
            
            # insertions <- sort(sample(length(main), n_chunks))
            insertions = sorted(random.sample(range(1, len(main) + 1), n_chunks))
            
            # for (i in rev(seq_along(insertions))) { main <- append(main, sub[[i]], insertions[i]) }
            # R append(x, value, after) inserts AFTER the index.
            for i in range(n_chunks - 1, -1, -1):
                pos = insertions[i] # 1-indexed
                main.insert(pos, chunked_sub[i])
        
        final_results.append(main_merge.join(main))
        
    return final_results if n > 1 else final_results[0]

# --- Execution ---

# Defaults to standard lorem ipsum
# r2py:entity:lorem_text
print(f"[1] \"{lorem_text()[0]}\"")

# Get two paragraphs of hangul (Korean)
# r2py:entity:lorem_text_1
res_hangul = lorem_text("hangul", 2)
for i, txt in enumerate(res_hangul):
    print(f"[{i+1}] \"{txt}\"")

# Get gibberish bi-directional text
# r2py:entity:lorem_bidi
print(f"[1] \"{lorem_bidi()}\"")
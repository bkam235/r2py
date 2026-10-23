import random

# Expanded mock datasets to better approximate the ids package
gfycat_adjectives = [
    "angry", "blue", "calm", "daring", "eager", "fancy", "great", "happy", "icy", "jolly",
    "chargeable", "teal", "frantic", "imminent", "shorted", "anarchic", "sedulous", 
    "halfpleased", "unanarchic", "superdesirous", "illogical", "defenceless", 
    "contradictable", "stomachy", "virile", "spicy", "blueish", "semiagricultural", 
    "nickel", "wafery", "saline", "zincic", "fur", "burnt", "feisty", "ash", "lean", 
    "wheat", "pelage", "ok", "teen", "sedate", "uppity", "peat", "left", "round", 
    "spy", "bardic", "leafed", "artful", "plain", "slight", "radon", "oozy", "adroit", 
    "ashy", "benign", "pretty", "next", "fresh", "dark", "zombie", "broke", "classy", 
    "firm", "vile", "blond", "weepy", "right", "privy"
]
gfycat_animals = [
    "aardvark", "bear", "cat", "dog", "elephant", "fox", "giraffe", "horse", "iguana", "jellyfish",
    "labradorretriever", "eland", "volvox", "chamois", "plankton", "galapagoshawk", 
    "bedbug", "howlermonkey", "fishingcat", "pullet", "easteuropeanshepherd", "goldfish", 
    "adder", "vixen", "eeve", "olingo", "moa", "cowrie", "puffin", "llama", "hen", "urial", 
    "ugandakob", "takin", "smelts", "millipede", "drever", "basil", "betafish", "moose", 
    "fugu", "asianconstablebutterfly", "puppy", "lemur", "turaco", "nene", "molly", 
    "cuckoo", "crow", "zander", "bison", "serval", "towhee"
]

# r2py:entity:adjective_animal
def toupper_camel(s):
    if not s: return s
    return s.capitalize()

def cases():
    return {
        "snake": {"join": "_", "tr": lambda x: x},
        "kebab": {"join": "-", "tr": lambda x: x},
        "dot": {"join": ".", "tr": lambda x: x},
        "camel": {"join": "", "tr": toupper_camel},
        "pascal": {"join": "", "tr": lambda x: x.capitalize()},
        "lower": {"join": " ", "tr": lambda x: x},
        "upper": {"join": " ", "tr": lambda x: x.upper()},
        "title": {"join": " ", "tr": lambda x: x.capitalize()},
        "sentence": {"join": " ", "tr": lambda x: x.capitalize()},
        "constant": {"join": "_", "tr": lambda x: x.upper()},
    }

def check_style(style):
    if not isinstance(style, str):
        raise TypeError("style must be a character vector")
    normalized = style.lower().replace("_case", "").replace("-case", "").replace("case", "")
    pos = cases()
    if normalized not in pos:
        raise ValueError(f"Invalid style '{style}'")
    return pos[normalized]

def make_combine(style):
    dat = check_style(style)
    join = dat["join"]
    tr = dat["tr"]
    
    def combine(x):
        if not x: return ""
        results = []
        num_rows = len(x[0])
        for i in range(num_rows):
            row_vals = []
            for col in range(len(x)):
                val = x[col][i]
                if style.lower() == "camel" and col == 0:
                    row_vals.append(val.lower())
                else:
                    row_vals.append(tr(val))
            results.append(join.join(row_vals))
        return results
    return combine

def ids_gen(n, vals, style="snake"):
    combine = make_combine(style)
    def gen(n_val=1):
        sampled_cols = [random.choices(v, k=n_val) for v in vals]
        res = combine(sampled_cols)
        return res if n_val > 1 else res[0]
    if n is None:
        return gen
    else:
        return gen(n)

def adjective_animal(n=1, n_adjectives=1, style="snake", max_len=float('inf')):
    adj_pool = gfycat_adjectives[:]
    ani_pool = gfycat_animals[:]
    
    if isinstance(max_len, (list, tuple)):
        m_adj, m_ani = max_len[0], max_len[1]
    else:
        m_adj = m_ani = max_len

    adj_pool = [a for a in adj_pool if len(a) <= m_adj]
    ani_pool = [a for a in ani_pool if len(a) <= m_ani]

    vals = [adj_pool] * n_adjectives + [ani_pool]
    return ids_gen(n, vals=vals, style=style)

def r_print(x):
    if isinstance(x, list):
        # Mimic R's vector printing: [1] "val1" "val2" ... [6] "val6"
        res = []
        current_line = []
        for i, val in enumerate(x, 1):
            if (i - 1) % 5 == 0:
                if current_line:
                    res.append(" ".join(current_line))
                    current_line = []
                res.append(f"[{i}]")
            current_line.append(f'"{val}"')
        if current_line:
            res.append(" ".join(current_line))
        
        # Join parts but handle the [1] prefix properly
        output = " ".join(res).replace("[1] ", "[1] ")
        print(output)
    else:
        print(f'[1] "{x}"')

# --- Execution ---

# Generate a random identifier:
# r2py:entity:adjective_animal
r_print(adjective_animal())

# Generate a bunch all at once:
# r2py:entity:adjective_animal_1
r_print(adjective_animal(5))

# Control the style of punctuation with the style argument:
# r2py:entity:adjective_animal_2
r_print(adjective_animal(style="lower"))
# r2py:entity:adjective_animal_3
r_print(adjective_animal(style="CONSTANT"))
# r2py:entity:adjective_animal_4
r_print(adjective_animal(style="camel"))
# r2py:entity:adjective_animal_5
r_print(adjective_animal(style="kebab"))

# Control the number of adjectives used
# r2py:entity:adjective_animal_6
r_print(adjective_animal(n_adjectives=3))

# This can get out of hand quickly though:
# r2py:entity:adjective_animal_7
r_print(adjective_animal(n_adjectives=7))

# Limit the length of adjectives and animals used:
# r2py:entity:adjective_animal_8
r_print(adjective_animal(10, max_len=6))

# The lengths can be controlled for adjectives and animals separately:
# r2py:entity:adjective_animal_9
r_print(adjective_animal(10, max_len=[6, float('inf')], n_adjectives=2))

# Pass n = NULL to bind arguments to a function
# r2py:entity:id
id_func = adjective_animal(None, n_adjectives=2, style="dot", max_len=6)
# r2py:entity:id_1
r_print(id_func())
# r2py:entity:id_2
r_print(id_func(10))
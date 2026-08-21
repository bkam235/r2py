# Translated from <R script> by r2py v0.3.0
# Model: ollama:gemma4:31b-cloud  ScriptMap entities: 3

import re
from typing import Any

def identity_transformer(text, envir):
    # Assuming identity_transformer returns a list/sequence based on the R length() check
    return [text]

# r2py:entity:vv_transformer
def vv_transformer(text, envir):
    regex = r"=$"
    if not re.search(regex, text):
        return identity_transformer(text, envir)

    # Remove the trailing '='
    text_clean = re.sub(regex, "", text)
    res = identity_transformer(text_clean, envir)
    
    n = len(res)
    # Join elements with comma
    res_str = ", ".join(map(str, res))
    
    if n > 1:
        res_str = f"[{res_str}]"
    
    return f"{text_clean} = {res_str}"
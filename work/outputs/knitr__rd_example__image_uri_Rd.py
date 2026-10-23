# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import os
import webbrowser
import base64
from pathlib import Path

# In Python, there is no exact equivalent to R.home("doc"), 
# but we can simulate the logic of getting a path to an image
# For this translation, we assume a placeholder image path or standard system path
# r2py:entity:uri
image_path = Path("logo.jpg") 

# Since image_uri in R converts an image to a data URI (base64), we implement that here
if image_path.exists():
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        uri = f"data:image/jpeg;base64,{encoded_string}"
else:
    # Fallback if file doesn't exist to avoid crash
    uri = "https://www.r-project.org/logo.jpg"

# cat(sprintf("<img src=\"%s\" />", uri), file = "logo.html")
# r2py:entity:cat
with open("logo.html", "w") as f:
    f.write(f'<img src="{uri}" />')

# browseURL("logo.html")
# r2py:entity:browseURL
webbrowser.open("file://" + os.path.realpath("logo.html"))
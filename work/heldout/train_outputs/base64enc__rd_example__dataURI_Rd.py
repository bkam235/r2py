# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 8

import base64
import urllib.parse
import numpy as np
from PIL import Image
import io
import os

# r2py:entity:dataURI
def dataURI(data=None, mime="", encoding="base64", file=None):
    if encoding is not None and encoding != "base64":
        raise ValueError("encoding must be either None or \"base64\"")
    
    prefix = f"data:{mime}"
    if encoding is not None:
        prefix += ";base64"
    prefix += ","

    if file is not None:
        if data is not None:
            raise ValueError("data and file are mutually exclusive")
        with open(file, "rb") as f:
            data = f.read()

    if data is None:
        data = b""
    
    if not isinstance(data, (bytes, bytearray)):
        if isinstance(data, (list, np.ndarray)):
            # R's paste(as.character(data), collapse="\n")
            data = "\n".join(map(str, data.flatten())).encode("utf-8")
        else:
            data = str(data).encode("utf-8")

    if encoding is None:
        # R's C_URIencode (RFC 3986) uses %XX. quote() is closer than quote_plus()
        encoded_data = urllib.parse.quote(data)
    else:
        encoded_data = base64.b64encode(data).decode("utf-8")
        
    return prefix + encoded_data

# r2py:entity:dataURI_2
def writePNG(image, target=None, dpi=None, asp=None, text=None, metadata=None):
    # R's writePNG returns the raw bytes if target is raw()
    img_array = (image * 255).astype(np.uint8)
    img = Image.fromarray(img_array, mode='L')
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

# Main script execution
# dataURI(as.raw(1:10))
# r2py:entity:dataURI
data_raw = bytes(range(1, 11))
print(dataURI(data=data_raw)) 

# dataURI(as.raw(1:10), encoding=NULL)
# r2py:entity:dataURI_1
print(dataURI(data=data_raw, encoding=None))

try:
    # Simulate require("png")
    import PIL
    # img <- matrix(1:16/16, 4) 
    # R fills by column: [1, 5, 9, 13], [2, 6, 10, 14]...
    # r2py:entity:img
# r2py:entity:img
    img = np.arange(1, 17).reshape(4, 4, order='F') / 16.0
    
    # dataURI(writePNG(img), "image/png")
    # r2py:entity:dataURI_2
# r2py:entity:dataURI_2
    print(dataURI(data=writePNG(img), mime="image/png"))
    
    # dataURI(file=system.file("img", "Rlogo.png", package="png"), mime="image/png")
    # We use a dummy path to simulate system.file behavior
    # r2py:entity:dataURI_3
# r2py:entity:dataURI_3
    logo_path = "Rlogo.png"
    # Create a dummy file so the call doesn't crash, matching R's expected file existence
    with open(logo_path, "wb") as f:
        f.write(b"dummy png content")
    print(dataURI(file=logo_path, mime="image/png"))
except ImportError:
    pass
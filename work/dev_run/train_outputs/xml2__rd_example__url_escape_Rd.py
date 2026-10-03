# Translated from <R script> by r2py v0.3.0
# Model: openrouter:google/gemma-4-31b-it  ScriptMap entities: 6

import urllib.parse

# url_escape("a b c")
# r2py:entity:url_escape
print(urllib.parse.quote("a b c"))

# url_escape("a b c", "")
# In R, the second argument to url_escape is often used to specify characters NOT to escape.
# In Python, 'safe' parameter defines characters that should be kept as-is.
# r2py:entity:url_escape_1
print(urllib.parse.quote("a b c", safe=""))

# url_unescape("a%20b%2fc")
# r2py:entity:url_unescape
print(urllib.parse.unquote("a%20b%2fc"))

# url_unescape("%C2%B5")
# r2py:entity:url_unescape_1
print(urllib.parse.unquote("%C2%B5"))
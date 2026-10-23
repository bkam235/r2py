# r2py crawler metadata
# package: xml2
# source_type: rd_example
# topic: url_escape.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xml2\help
# lines: 6

suppressPackageStartupMessages(library(xml2))
url_escape("a b c")
url_escape("a b c", "")

url_unescape("a%20b%2fc")
url_unescape("%C2%B5")
# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: string.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 17

suppressPackageStartupMessages(library(rlang))
# As everywhere in R, you can specify a string with Unicode
# escapes. The characters corresponding to Unicode codepoints will
# be encoded in UTF-8, and the string will be marked as UTF-8
# automatically:
cafe <- string("caf\uE9")
Encoding(cafe)
charToRaw(cafe)

# In addition, string() provides useful conversions to let
# programmers control how the string is represented in memory. For
# encodings other than UTF-8, you'll need to supply the bytes in
# hexadecimal form. If it is a latin1 encoding, you can mark the
# string explicitly:
cafe_latin1 <- string(c(0x63, 0x61, 0x66, 0xE9), "latin1")
Encoding(cafe_latin1)
charToRaw(cafe_latin1)
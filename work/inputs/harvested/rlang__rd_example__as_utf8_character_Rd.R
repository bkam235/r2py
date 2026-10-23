# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: as_utf8_character.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 6

suppressPackageStartupMessages(library(rlang))
# Let's create a string marked as UTF-8 (which is guaranteed by the
# Unicode escaping in the string):
utf8 <- "caf\uE9"
Encoding(utf8)
charToRaw(utf8)
# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: chr_unserialise_unicode.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 5

suppressPackageStartupMessages(library(rlang))
ascii <- "<U+5E78>"
chr_unserialise_unicode(ascii)

identical(chr_unserialise_unicode(ascii), "\u5e78")
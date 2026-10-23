# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: raw_deparse_str.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 4

suppressPackageStartupMessages(library(rlang))
raw_deparse_str(raw())
raw_deparse_str(charToRaw("string"))
raw_deparse_str(raw(10), prefix = "'0x", suffix = "'")
# r2py crawler metadata
# package: farver
# source_type: rd_example
# topic: native_encoding.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\farver\help
# lines: 7

suppressPackageStartupMessages(library(farver))
# Get native representation of navyblue and #228B22
native_col <- encode_native(c('navyblue', '#228B22'))
native_col

# Convert back
decode_native(native_col)
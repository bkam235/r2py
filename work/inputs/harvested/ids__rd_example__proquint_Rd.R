# r2py crawler metadata
# package: ids
# source_type: rd_example
# topic: proquint.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ids\help
# lines: 9

suppressPackageStartupMessages(library(ids))
# A single, two word, proquint
proquint()

# Longer identifier:
proquint(n_words = 5)

# More identifiers
proquint(10)
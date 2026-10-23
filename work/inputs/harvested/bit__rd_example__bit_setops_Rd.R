# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bit_setops.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 7

suppressPackageStartupMessages(library(bit))
bit_union(1:2, 2:3)
bit_intersect(1:2, 2:3)
bit_setdiff(1:2, 2:3)
bit_symdiff(1:2, 2:3)
bit_setequal(1:2, 2:3)
bit_setequal(1:2, 2:1)
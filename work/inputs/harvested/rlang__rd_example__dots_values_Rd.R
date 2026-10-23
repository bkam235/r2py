# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: dots_values.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 6

suppressPackageStartupMessages(library(rlang))
dots <- dots_values(!!! list(1, 2), 3)
dots

# Flatten the objects marked as spliced:
flatten_if(dots, is_spliced)
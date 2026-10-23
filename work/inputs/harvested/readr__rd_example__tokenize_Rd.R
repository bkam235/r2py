# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: tokenize.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 5

suppressPackageStartupMessages(library(readr))
tokenize("1,2\n3,4,5\n\n6")

# Only tokenize first two lines
tokenize("1,2\n3,4,5\n\n6", n = 2)
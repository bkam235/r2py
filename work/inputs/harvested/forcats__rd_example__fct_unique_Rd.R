# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_unique.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 8

suppressPackageStartupMessages(library(forcats))
f <- fct(letters[rpois(100, 10)])
unique(f)     # in order of appearance
fct_unique(f) # in order of levels

f <- fct(letters[rpois(100, 2)], letters[1:20])
unique(f)     # levels that appear in data
fct_unique(f) # all possible levels
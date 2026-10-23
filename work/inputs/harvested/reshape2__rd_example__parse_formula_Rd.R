# r2py crawler metadata
# package: reshape2
# source_type: rd_example
# topic: parse_formula.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\reshape2\help
# lines: 4

suppressPackageStartupMessages(library(reshape2))
reshape2:::parse_formula("a + ...", letters[1:6])
reshape2:::parse_formula("a ~ b + d")
reshape2:::parse_formula("a + b ~ c ~ .")
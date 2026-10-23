# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: pat_fun.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 7

suppressPackageStartupMessages(library(knitr))
# see how knit_patterns is modified
knit_patterns$get()
pat_rnw()
knit_patterns$get()

knit_patterns$restore()  # empty the list
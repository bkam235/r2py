# r2py crawler metadata
# package: knitr
# source_type: rd_example
# topic: all_labels.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\knitr\help
# lines: 7

suppressPackageStartupMessages(library(knitr))
# the examples below are meaningless unless you put them in a knitr document
all_labels()
all_labels(engine == "Rcpp")
all_labels(echo == FALSE && results != "hide")
# or separate the two conditions
all_labels(echo == FALSE, results != "hide")
# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: downSample.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 7

suppressPackageStartupMessages(library(caret))
## A ridiculous example...
data(oil)
table(oilType)
downSample(fattyAcids, oilType)

upSample(fattyAcids, oilType)
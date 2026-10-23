# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: crModel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 5

suppressPackageStartupMessages(library(prodlim))
library(lava)
m <- crModel()
d <- sim(m,6)
print(d)
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: Model.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 4

suppressPackageStartupMessages(library(lava))
m <- lvm(y~x)
e <- estimate(m, sim(m,100))
Model(e)
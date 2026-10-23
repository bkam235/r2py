# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: ordreg.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
m <- lvm(y~x)
ordinal(m,K=3) <- ~y
d <- sim(m,100)
e <- ordreg(y~x,d)
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: IC.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 6

suppressPackageStartupMessages(library(lava))
m <- lvm(y~x+z)
distribution(m, ~y+z) <- binomial.lvm("logit")
d <- sim(m,1e3)
g <- glm(y~x+z,data=d,family=binomial)
var_ic(IC(g))
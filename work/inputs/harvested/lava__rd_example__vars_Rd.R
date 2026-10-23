# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: vars.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
g <- lvm(eta1 ~ x1+x2)
regression(g) <- c(y1,y2,y3) ~ eta1
latent(g) <- ~eta1
endogenous(g)
exogenous(g)
identical(latent(g), setdiff(vars(g),manifest(g)))
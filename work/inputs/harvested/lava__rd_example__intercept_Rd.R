# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: intercept.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
## A multivariate model
m <- lvm(c(y1,y2) ~ f(x1,beta)+x2)
regression(m) <- y3 ~ f(x1,beta)
intercept(m) <- y1 ~ f(mu)
intercept(m, ~y2+y3) <- list(2,"mu")
intercept(m) ## Examine intercepts of model (NA translates to free/unique paramete##r)
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: ordinal-set.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
if (requireNamespace("mets")) {
m <- lvm(y + z ~ x + 1*u[0], latent=~u)
ordinal(m, K=3) <- ~y+z
d <- sim(m, 100, seed=1)
e <- estimate(m, d)
}
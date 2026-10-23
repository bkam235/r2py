# r2py crawler metadata
# package: lava
# source_type: vignette
# topic: nonlinear_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\doc\nonlinear.R
# lines: 7

suppressPackageStartupMessages(library(lava))
f <- function(x) cos(1.25*x) + x - 0.25*x^2
m <- lvm(x1+x2+x3 ~ eta1, y1+y2+y3 ~ eta2, latent=~eta1+eta2)
regression(m) <- eta1+eta2 ~ z
functional(m, eta2~eta1) <- f

d <- sim(m, n=200, seed=42) # Default is all parameters are 1
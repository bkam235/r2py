# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: complik.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
m <- lvm(c(y1,y2,y3)~b*x+1*u[0],latent=~u)
ordinal(m,K=2) <- ~y1+y2+y3
d <- sim(m,50,seed=1)
if (requireNamespace("mets", quietly=TRUE)) {
   e1 <- complik(m,d,control=list(trace=1),type="all")
}
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: twostageCV.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 14

suppressPackageStartupMessages(library(lava))
## Reduce Ex.Timings##'
m1 <- lvm( x1+x2+x3 ~ u, latent= ~u)
m2 <- lvm( y ~ 1 )
m <- functional(merge(m1,m2), y ~ u, value=function(x) sin(x)+x)
distribution(m, ~u1) <- uniform.lvm(-6,6)
d <- sim(m,n=500,seed=1)
nonlinear(m2) <- y~u1
if (requireNamespace('mets', quietly=TRUE)) {
  set.seed(1)
  val <- twostageCV(m1, m2, data=d, std.err=FALSE, df=2:6, nmix=1:2,
                  nfolds=2)
  val
}
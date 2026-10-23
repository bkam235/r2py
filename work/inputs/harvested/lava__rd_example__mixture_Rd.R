# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: mixture.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 17

suppressPackageStartupMessages(library(lava))
m0 <- lvm(list(y~x+z,x~z))
distribution(m0,~z) <- binomial.lvm()
d <- sim(m0,2000,p=c("y~z"=2,"y~x"=1),seed=1)

## unmeasured confounder example
m <- baptize(lvm(y~x, x~1));
intercept(m,~x+y) <- NA

if (requireNamespace('mets', quietly=TRUE)) {
  set.seed(42)
  M <- mixture(m,k=2,data=d,control=list(trace=1,tol=1e-6))
  summary(M)
  lm(y~x,d)
  estimate(M,"y~x")
  ## True slope := 1
}
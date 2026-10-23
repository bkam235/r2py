# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: stack.estimate.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 11

suppressPackageStartupMessages(library(lava))
m <- lvm(z0~x)
Missing(m, z ~ z0) <- r~x
distribution(m,~x) <- binomial.lvm()
p <- c(r=-1,'r~x'=0.5,'z0~x'=2)
beta <- p[3]/2
d <- sim(m,500,p=p,seed=1)
m1 <- estimate(r~x,data=d,family=binomial)
d$w <- d$r/predict(m1,type="response")
m2 <- estimate(z~1, weights=w, data=d)
(e <- stack(m1,m2,propensity=TRUE))
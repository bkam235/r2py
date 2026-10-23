# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: gof.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 18

suppressPackageStartupMessages(library(lava))
m <- lvm(list(y~v1+v2+v3+v4,c(v1,v2,v3,v4)~x))
set.seed(1)
dd <- sim(m,1000)
e <- estimate(m, dd)
gof(e,all=TRUE,rmsea.threshold=0.05,level=0.9)


set.seed(1)
m <- lvm(list(c(y1,y2,y3)~u,y1~x)); latent(m) <- ~u
regression(m,c(y2,y3)~u) <- "b"
d <- sim(m,1000)
e <- estimate(m,d)
rsq(e)
##'
rr <- rsq(e,TRUE)
rr
estimate(rr,contrast=rbind(c(1,-1,0),c(1,0,-1),c(0,1,-1)))
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: partialcor.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 5

suppressPackageStartupMessages(library(lava))
m <- lvm(c(y1,y2,y3)~x1+x2)
covariance(m) <- c(y1,y2,y3)~y1+y2+y3
d <- sim(m,500)
partialcor(~x1+x2,d)
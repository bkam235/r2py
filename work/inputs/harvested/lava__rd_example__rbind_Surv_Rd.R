# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: rbind.Surv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 10

suppressPackageStartupMessages(library(lava))
y <- yl <- yr <- rnorm(10)
yl[1:5] <- NA; yr[6:10] <- NA
S1 <- survival::Surv(yl,yr,type="interval2")
S2 <- survival::Surv(y,y>0,type="right")
S3 <- survival::Surv(y,y<0,type="left")

rbind(S1,S1)
rbind(S2,S2)
rbind(S3,S3)
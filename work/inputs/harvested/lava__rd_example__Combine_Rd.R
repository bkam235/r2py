# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: Combine.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 8

suppressPackageStartupMessages(library(lava))
data(serotonin)
m1 <- lm(cau ~ age*gene1 + age*gene2,data=serotonin)
m2 <- lm(cau ~ age + gene1,data=serotonin)
m3 <- lm(cau ~ age*gene2,data=serotonin)

Combine(list(A=m1,B=m2,C=m3),fun=function(x)
     c("_____"="",R2=" "%++%format(summary(x)$r.squared,digits=2)))
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: closed_testing.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 20

suppressPackageStartupMessages(library(lava))
m <- lvm()
regression(m, c(y1,y2,y3,y4)~x) <- c(0, 0.25, 0, 0.25)
regression(m, to=endogenous(m), from="u") <- 1
variance(m,endogenous(m)) <- 1
set.seed(1)
d <- sim(m, 200)
l1 <- lm(y1~x,d)
l2 <- lm(y2~x,d)
l3 <- lm(y3~x,d)
l4 <- lm(y4~x,d)

(a <- merge(l1, l2, l3, l4, subset=2))
if (requireNamespace("mets",quietly=TRUE)) {
   alpha_zmax(a)
}
adj <- closed_testing(a)
adj
adj$p.value
summary(adj)
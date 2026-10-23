# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: confint.lvmfit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 9

suppressPackageStartupMessages(library(lava))
m <- lvm(y~x)
d <- sim(m,100)
e <- estimate(lvm(y~x), d)
confint(e,3,profile=TRUE)
confint(e,3)
 ## Reduce Ex.timings
B <- bootstrap(e,R=50)
B
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: bootstrap.lvm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
m <- lvm(y~x)
d <- sim(m,100)
e <- estimate(lvm(y~x), data=d)
 ## Reduce Ex.Timings
B <- bootstrap(e,R=50,mc.cores=1)
B
# r2py crawler metadata
# package: lava
# source_type: rd_example
# topic: intervention.lvm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\lava\help
# lines: 7

suppressPackageStartupMessages(library(lava))
m <- lvm(y ~ a + x, a ~ x)
distribution(m, ~a+y) <- binomial.lvm()
mm <- intervention(m, "a", value=3)
sim(mm, 10)
mm <- intervention(m, a~x, function(x) (x>0)*1)
sim(mm, 10)
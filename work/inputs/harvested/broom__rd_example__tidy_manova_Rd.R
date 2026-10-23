# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: tidy.manova.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 4

suppressPackageStartupMessages(library(broom))
npk2 <- within(npk, foo <- rnorm(24))
m <- manova(cbind(yield, foo) ~ block + N * P * K, npk2)
tidy(m)
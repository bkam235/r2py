# r2py crawler metadata
# package: broom
# source_type: rd_example
# topic: summary_tidiers.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\broom\help
# lines: 10

suppressPackageStartupMessages(library(broom))
v <- rnorm(1000)
s <- summary(v)
s

tidy(s)
glance(s)

v2 <- c(v,NA)
tidy(summary(v2))
# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: transform_log.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 15

suppressPackageStartupMessages(library(scales))
plot(transform_log2(), xlim = c(0, 5))
plot(transform_log(), xlim = c(0, 5))
plot(transform_log10(), xlim = c(0, 5))

plot(transform_log(), xlim = c(0, 2))
plot(transform_log1p(), xlim = c(-1, 1))

# The pseudo-log is defined for all real numbers
plot(transform_pseudo_log(), xlim = c(-5, 5))
lines(transform_log(), xlim = c(0, 5), col = "red")

# For large positives numbers it's very close to log
plot(transform_pseudo_log(), xlim = c(1, 20))
lines(transform_log(), xlim = c(1, 20), col = "red")
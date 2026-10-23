# r2py crawler metadata
# package: scales
# source_type: rd_example
# topic: transform_boxcox.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\scales\help
# lines: 10

suppressPackageStartupMessages(library(scales))
plot(transform_boxcox(-1), xlim = c(0, 10))
plot(transform_boxcox(0), xlim = c(0, 10))
plot(transform_boxcox(1), xlim = c(0, 10))
plot(transform_boxcox(2), xlim = c(0, 10))

plot(transform_modulus(-1), xlim = c(-10, 10))
plot(transform_modulus(0), xlim = c(-10, 10))
plot(transform_modulus(1), xlim = c(-10, 10))
plot(transform_modulus(2), xlim = c(-10, 10))
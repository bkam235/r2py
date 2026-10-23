# r2py crawler metadata
# package: ggplot2
# source_type: rd_example
# topic: hmisc.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\help
# lines: 9

suppressPackageStartupMessages(library(ggplot2))
if (requireNamespace("Hmisc", quietly = TRUE)) {
set.seed(1)
x <- rnorm(100)
mean_cl_boot(x)
mean_cl_normal(x)
mean_sdl(x)
median_hilow(x)
}
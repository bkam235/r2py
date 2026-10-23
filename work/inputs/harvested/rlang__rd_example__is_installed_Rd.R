# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: is_installed.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 4

suppressPackageStartupMessages(library(rlang))
is_installed("utils")
is_installed(c("base", "ggplot5"))
is_installed(c("base", "ggplot5"), version = c(NA, "5.1.0"))
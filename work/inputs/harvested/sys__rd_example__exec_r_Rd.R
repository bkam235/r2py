# r2py crawler metadata
# package: sys
# source_type: rd_example
# topic: exec_r.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\sys\help
# lines: 11

suppressPackageStartupMessages(library(sys))
# Hello world
r_wait("--version")

# Run some code
r_wait(c('--vanilla', '-q', '-e', 'sessionInfo()'))

# Run a script via stdin
tmp <- tempfile()
writeLines(c("x <- rnorm(100)", "mean(x)"), con = tmp)
r_wait(std_in = tmp)
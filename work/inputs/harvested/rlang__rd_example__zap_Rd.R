# r2py crawler metadata
# package: rlang
# source_type: rd_example
# topic: zap.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\rlang\help
# lines: 7

suppressPackageStartupMessages(library(rlang))
# Create one zap object:
zap()

# Create a list of zaps:
rep(list(zap()), 3)
rep_named(c("foo", "bar"), list(zap()))
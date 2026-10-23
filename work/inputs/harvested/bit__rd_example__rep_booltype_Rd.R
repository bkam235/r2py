# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: rep.booltype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 5

suppressPackageStartupMessages(library(bit))
rep(as.bit(c(FALSE, TRUE)), 2)
 rep(as.bit(c(FALSE, TRUE)), length.out=7)
 rep(as.bitwhich(c(FALSE, TRUE)), 2)
 rep(as.bitwhich(c(FALSE, TRUE)), length.out=1)
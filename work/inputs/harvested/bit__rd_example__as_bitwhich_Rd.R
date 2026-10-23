# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: as.bitwhich.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 9

suppressPackageStartupMessages(library(bit))
as.bitwhich(c(0L, 1L, 2L, -2L, NA))
as.bitwhich(c(0, 1, 2, -2, NA))

 as.bitwhich(c(NA, NA, NA))
 as.bitwhich(c(FALSE, FALSE, FALSE))
 as.bitwhich(c(FALSE, FALSE, TRUE))
 as.bitwhich(c(FALSE, TRUE, TRUE))
 as.bitwhich(c(TRUE, TRUE, TRUE))
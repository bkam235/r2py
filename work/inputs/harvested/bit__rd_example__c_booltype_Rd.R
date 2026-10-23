# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: c.booltype.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
c(bit(4), !bit(4))
 c(bit(4), !bitwhich(4))
 c(bitwhich(4), !bit(4))
 c(ri(1, 2, 4), !bit(4))
 c(bit(4), !logical(4))
 message("logical in first argument does not dispatch: c(logical(4), bit(4))")
 c.booltype(logical(4), !bit(4))
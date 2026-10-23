# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: bitwhich.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
bitwhich()
bitwhich(12)
bitwhich(12, x=TRUE)
bitwhich(12, x=3)
bitwhich(12, x=-3)
bitwhich(12, x=integer())
bitwhich(12, x=integer(), xempty=TRUE)
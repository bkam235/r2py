# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: write_file.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 6

suppressPackageStartupMessages(library(brio))
tf <- tempfile()

write_file("some data\n", tf)

unlink(tf)
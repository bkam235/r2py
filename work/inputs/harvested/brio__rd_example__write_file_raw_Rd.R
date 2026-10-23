# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: write_file_raw.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 6

suppressPackageStartupMessages(library(brio))
tf <- tempfile()

write_file_raw(as.raw(c(0x66, 0x6f, 0x6f, 0x0, 0x62, 0x61, 0x72)), tf)

unlink(tf)
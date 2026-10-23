# r2py crawler metadata
# package: fansi
# source_type: rd_example
# topic: fansi_lines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\fansi\help
# lines: 4

suppressPackageStartupMessages(library(fansi))
NEWS <- readLines(file.path(R.home('doc'), 'NEWS'))
writeLines(fansi_lines(NEWS[1:20]))
writeLines(fansi_lines(NEWS[1:20], step=8))
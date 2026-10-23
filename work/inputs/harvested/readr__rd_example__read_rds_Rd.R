# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: read_rds.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 6

suppressPackageStartupMessages(library(readr))
temp <- tempfile()
write_rds(mtcars, temp)
read_rds(temp)

write_rds(mtcars, "compressed_mtc.rds", "xz", compression = 9L)
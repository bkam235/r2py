# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: read_delim_chunked.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 4

suppressPackageStartupMessages(library(readr))
# Cars with 3 gears
f <- function(x, pos) subset(x, gear == 3)
read_csv_chunked(readr_example("mtcars.csv"), DataFrameCallback$new(f), chunk_size = 5)
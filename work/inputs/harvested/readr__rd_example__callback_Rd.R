# r2py crawler metadata
# package: readr
# source_type: rd_example
# topic: callback.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\readr\help
# lines: 23

suppressPackageStartupMessages(library(readr))
## If given a regular function it is converted to a SideEffectChunkCallback

# view structure of each chunk
read_lines_chunked(readr_example("mtcars.csv"), str, chunk_size = 5)

# Print starting line of each chunk
f <- function(x, pos) print(pos)
read_lines_chunked(readr_example("mtcars.csv"), SideEffectChunkCallback$new(f), chunk_size = 5)

# If combined results are desired you can use the DataFrameCallback

# Cars with 3 gears
f <- function(x, pos) subset(x, gear == 3)
read_csv_chunked(readr_example("mtcars.csv"), DataFrameCallback$new(f), chunk_size = 5)

# The ListCallback can be used for more flexible output
f <- function(x, pos) x$mpg[x$hp > 100]
read_csv_chunked(readr_example("mtcars.csv"), ListCallback$new(f), chunk_size = 5)

# The AccumulateCallback accumulates results from each chunk
f <- function(x, pos, acc) sum(x$mpg) + acc
read_csv_chunked(readr_example("mtcars.csv"), AccumulateCallback$new(f, acc = 0), chunk_size = 5)
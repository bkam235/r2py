# r2py crawler metadata
# package: dplyr
# source_type: rd_example
# topic: ntile.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\help
# lines: 10

suppressPackageStartupMessages(library(dplyr))
x <- c(5, 1, 3, 2, 2, NA)
ntile(x, 2)
ntile(x, 4)

# If the bucket sizes are uneven, the larger buckets come first
ntile(1:8, 3)

# Ties are ignored
ntile(rep(1, 8), 3)
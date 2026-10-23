# r2py crawler metadata
# package: brio
# source_type: rd_example
# topic: writeLines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\brio\help
# lines: 14

suppressPackageStartupMessages(library(brio))
tf <- tempfile()

writeLines(rownames(mtcars), tf)

# Trying to use connections throws an error
con <- file(tf)
try(writeLines(con))
close(con)

# Trying to use unsupported args throws a warning
writeLines(rownames(mtcars), tf, useBytes = TRUE)

unlink(tf)
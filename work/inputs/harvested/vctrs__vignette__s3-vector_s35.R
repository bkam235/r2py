# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s35
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 9

suppressPackageStartupMessages(library(vctrs))
x <- as.POSIXlt(ISOdatetime(2020, 1, 1, 0, 0, 1:3))
x

length(x)
length(unclass(x))

x[[1]] # the first date time
unclass(x)[[1]] # the first component, the number of seconds
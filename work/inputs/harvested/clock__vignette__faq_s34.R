# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: faq_s34
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\faq.R
# lines: 8

suppressPackageStartupMessages(library(clock))
x <- as.POSIXct("2019-01-01", "America/New_York")

# POSIXct is implemented as a double
unclass(x)

# POSIXlt is a record type
unclass(as.POSIXlt(x))
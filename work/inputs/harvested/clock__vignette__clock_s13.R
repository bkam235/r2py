# r2py crawler metadata
# package: clock
# source_type: vignette
# topic: clock_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\clock\doc\clock.R
# lines: 5

suppressPackageStartupMessages(library(clock))
x <- c("2020/1/5", "10-03-05", "2020/2/2")
formats <- c("%Y/%m/%d", "%y-%m-%d")

date_parse(x, format = formats)
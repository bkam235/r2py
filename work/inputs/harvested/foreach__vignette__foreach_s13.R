# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 4

suppressPackageStartupMessages(library(foreach))
library(iterators)
x <- foreach(a=irnorm(4, count=4), .combine='cbind') %do% a
x
# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s5
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 5

suppressPackageStartupMessages(library(foreach))
x <- foreach(a=1:1000, b=rep(10, 2)) %do% {
  a + b
}
x
# r2py crawler metadata
# package: foreach
# source_type: vignette
# topic: foreach_s15
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\foreach\doc\foreach.R
# lines: 9

suppressPackageStartupMessages(library(foreach))
set.seed(123)
x <- numeric(4)
i <- 0
while (i < 1000) {
  x <- x + rnorm(4)
  i <- i + 1
}
x
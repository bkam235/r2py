# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: isplit.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 11

suppressPackageStartupMessages(library(iterators))
x <- rnorm(200)
f <- factor(sample(1:10, length(x), replace=TRUE))

it <- isplit(x, f)
expected <- split(x, f)

for (i in expected) {
  actual <- nextElem(it)
  stopifnot(actual$value == i)
}
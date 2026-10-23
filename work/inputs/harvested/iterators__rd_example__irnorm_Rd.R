# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: irnorm.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 7

suppressPackageStartupMessages(library(iterators))
# create an iterator that returns three random numbers
  it <- irnorm(1, count=3)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  try(nextElem(it))  # expect a StopIteration exception
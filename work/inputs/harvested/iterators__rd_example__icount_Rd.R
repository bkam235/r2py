# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: icount.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 7

suppressPackageStartupMessages(library(iterators))
# create an iterator that counts from 1 to 3.
  it <- icount(3)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  try(nextElem(it))  # expect a StopIteration exception
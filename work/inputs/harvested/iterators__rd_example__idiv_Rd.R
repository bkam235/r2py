# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: idiv.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 15

suppressPackageStartupMessages(library(iterators))
# divide the value 10 into 3 pieces
  it <- idiv(10, chunks=3)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  try(nextElem(it))  # expect a StopIteration exception

  # divide the value 10 into pieces no larger than 3
  it <- idiv(10, chunkSize=3)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  try(nextElem(it))  # expect a StopIteration exception
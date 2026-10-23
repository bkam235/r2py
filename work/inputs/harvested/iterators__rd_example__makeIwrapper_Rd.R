# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: makeIwrapper.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 11

suppressPackageStartupMessages(library(iterators))
# create an iterator maker for the sample function
  mysample <- makeIwrapper('sample')
  # use this iterator maker to generate an iterator
  # that will generate three five member samples from the
  # sequence 1:100
  it <- mysample(1:100, 5, count=3)
  nextElem(it)
  nextElem(it)
  nextElem(it)
  try(nextElem(it))  # expect a StopIteration exception
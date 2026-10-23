# r2py crawler metadata
# package: iterators
# source_type: rd_example
# topic: ireadLines.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\iterators\help
# lines: 6

suppressPackageStartupMessages(library(iterators))
# create an iterator over the lines of COPYING
  it <- ireadLines(file.path(R.home(), 'COPYING'))
  nextElem(it)
  nextElem(it)
  nextElem(it)
# r2py crawler metadata
# package: base64enc
# source_type: rd_example
# topic: base64.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\base64enc\help
# lines: 7

suppressPackageStartupMessages(library(base64enc))
base64encode(1:100)
  base64encode(1:100, 70)
  base64encode(1:100, 70, "\n")
  x <- charToRaw("the decoded content, otherwise the number of bytes")
  y <- base64decode(base64encode(x))
  stopifnot(identical(x, y))
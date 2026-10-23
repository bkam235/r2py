# r2py crawler metadata
# package: bit
# source_type: rd_example
# topic: vecseq.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\help
# lines: 8

suppressPackageStartupMessages(library(bit))
sequence(c(3, 4))
  vecseq(c(3, 4))
  vecseq(c(1, 11), c(5, 15))
  vecseq(c(1, 11), c(5, 15), concat=FALSE, eval=FALSE)
  vecseq(c(1, 11), c(5, 15), concat=FALSE, eval=TRUE)
  vecseq(c(1, 11), c(5, 15), concat=TRUE, eval=FALSE)
  vecseq(c(1, 11), c(5, 15), concat=TRUE, eval=TRUE)
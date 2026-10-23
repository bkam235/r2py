# r2py crawler metadata
# package: plyr
# source_type: rd_example
# topic: rbind.fill.matrix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\plyr\help
# lines: 12

suppressPackageStartupMessages(library(plyr))
A <- matrix (1:4, 2)
B <- matrix (6:11, 2)
A
B
rbind.fill.matrix (A, B)

colnames (A) <- c (3, 1)
A
rbind.fill.matrix (A, B)

rbind.fill.matrix (A, 99)
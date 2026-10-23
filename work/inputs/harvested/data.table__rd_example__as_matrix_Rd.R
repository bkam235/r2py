# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: as.matrix.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 9

suppressPackageStartupMessages(library(data.table))
DT <- data.table(A = letters[1:10], X = 1:10, Y = 11:20)
as.matrix(DT) # character matrix
as.matrix(DT, rownames = "A")
as.matrix(DT, rownames = 1)
as.matrix(DT, rownames = TRUE)

setkey(DT, A)
as.matrix(DT, rownames = TRUE)
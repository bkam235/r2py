# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: setcolorder.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 16

suppressPackageStartupMessages(library(data.table))
set.seed(45L)
DT = data.table(A=sample(3, 10, TRUE),
         B=sample(letters[1:3], 10, TRUE), C=sample(10))

setcolorder(DT, c("C", "A", "B"))

#incomplete specification
setcolorder(DT, "A")

# insert new column as first column
set(DT, j="D", value=sample(10))
setcolorder(DT, "D", before=1)

# move column to last column place
setcolorder(DT, "A", after=ncol(DT))
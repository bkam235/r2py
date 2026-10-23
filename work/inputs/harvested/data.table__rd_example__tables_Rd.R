# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: tables.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 5

suppressPackageStartupMessages(library(data.table))
DT = data.table(A=1:10, B=letters[1:10])
DT2 = data.table(A=1:10000, ColB=10000:1)
setkey(DT,B)
tables()
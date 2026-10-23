# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: last.updated.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 9

suppressPackageStartupMessages(library(data.table))
d = data.table(a=1:4, b=2:5)
d[2:3, z:=5L]
.Last.updated

# updated count takes duplicates into account #2837
DT = data.table(a = 1L)
DT[c(1L, 1L), a := 2:3]
.Last.updated
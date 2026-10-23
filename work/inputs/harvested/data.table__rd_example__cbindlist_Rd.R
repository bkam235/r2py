# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: cbindlist.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 9

suppressPackageStartupMessages(library(data.table))
d1 = data.table(x=1:3, v1=1L, key="x")
d2 = data.table(y=3:1, v2=2L, key="y")
d3 = data.table(z=2:4, v3=3L)
cbindlist(list(d1, d2, d3))
cbindlist(list(d1, d1))
d4 = setcbindlist(list(d1))
d4[, v1:=2L]
identical(d4, d1)
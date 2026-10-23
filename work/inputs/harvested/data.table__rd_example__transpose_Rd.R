# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: transpose.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 18

suppressPackageStartupMessages(library(data.table))
ll = list(1:5, 6:8)
transpose(ll)
setDT(transpose(ll, fill=0))[]

DT = data.table(x=1:5, y=6:10)
transpose(DT)

DT = data.table(x=1:3, y=c("a","b","c"))
transpose(DT, list.cols=TRUE)

# base R equivalent of transpose
l = list(1:3, c("a", "b", "c"))
lapply(seq(length(l[[1]])), function(x) lapply(l, `[[`, x))
transpose(l, list.cols=TRUE)

ll = list(nm=c('x', 'y'), 1:2, 3:4)
transpose(ll, make.names="nm")
# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: frolladapt.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 15

suppressPackageStartupMessages(library(data.table))
idx = as.Date("2022-10-23") + c(0,1,4,5,6,7,9,10,14)
dt = data.table(index=idx, value=seq_along(idx))
dt
dt[, n3 := frolladapt(index, n=3L)]
dt
dt[, rollmean3 := frollmean(value, n3, adaptive=TRUE)]
dt
dt[, n3p := frolladapt(index, n=3L, partial=TRUE)]
dt[, rollmean3p := frollmean(value, n3p, adaptive=TRUE)]
dt

n34 = frolladapt(idx, c(small=3, big=4), give.names=TRUE)
n34
dt[, frollmean(value, n34, adaptive=TRUE, give.names=TRUE)]
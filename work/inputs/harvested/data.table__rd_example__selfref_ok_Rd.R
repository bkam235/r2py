# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: selfref.ok.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 17

suppressPackageStartupMessages(library(data.table))
d1 = structure(list(V1=1L), class=c("data.table","data.frame"))
.selfref.ok(d1)
setDT(d1)
.selfref.ok(d1)

saveRDS(d1, f<-tempfile())
d2 = readRDS(f)
.selfref.ok(d2)
invisible(file.remove(f))
setDT(d2)
.selfref.ok(d2)

d3 = unserialize(serialize(d2, NULL))
.selfref.ok(d3)
setDT(d3)
.selfref.ok(d3)
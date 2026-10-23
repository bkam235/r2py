# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: groupingsets.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 37

suppressPackageStartupMessages(library(data.table))
n = 24L
set.seed(25)
DT <- data.table(
  color = sample(c("green","yellow","red"), n, TRUE),
  year = as.Date(sample(paste0(2011:2015,"-01-01"), n, TRUE)),
  status = as.factor(sample(c("removed","active","inactive","archived"), n, TRUE)),
  amount = sample(1:5, n, TRUE),
  value = sample(c(3, 3.5, 2.5, 2), n, TRUE)
)

# rollup
by_vars = c("color", "year", "status")
rollup(DT, j=sum(value), by=by_vars) # default id=FALSE
rollup(DT, j=sum(value), by=by_vars, id=TRUE)
rollup(DT, j=lapply(.SD, sum), by=by_vars, id=TRUE, .SDcols="value")
rollup(DT, j=c(list(count=.N), lapply(.SD, sum)), by=by_vars, id=TRUE)
rollup(DT, j=sum(value), by=by_vars,
       # specify label by variable name
       label=list(color="total", year=as.Date("3000-01-01"), status=factor("total")))
rollup(DT, j=sum(value), by=by_vars,
       # specify label by variable name and first element of class
       label=list(color="total", Date=as.Date("3000-01-01"), factor=factor("total")))
# label is character scalar so applies to color only
rollup(DT, j=sum(value), by=by_vars, label="total")
rollup(DT, j=.N, by=c("color", "year", "status", "value"),
       # label can be explicitly specified as NA or NaN
       label = list(color=NA_character_, year=as.Date(NA), status=factor(NA), value=NaN))

# cube
cube(DT, j = sum(value), by = c("color","year","status"), id=TRUE)
cube(DT, j = lapply(.SD, sum), by = c("color","year","status"), id=TRUE, .SDcols="value")
cube(DT, j = c(list(count=.N), lapply(.SD, sum)), by = c("color","year","status"), id=TRUE)

# groupingsets
groupingsets(DT, j = c(list(count=.N), lapply(.SD, sum)), by = c("color","year","status"),
             sets = list("color", c("year","status"), character()), id=TRUE)
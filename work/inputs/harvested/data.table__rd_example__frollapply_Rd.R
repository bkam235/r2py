# r2py crawler metadata
# package: data.table
# source_type: rd_example
# topic: frollapply.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\data.table\help
# lines: 27

suppressPackageStartupMessages(library(data.table))
frollapply(1:16, 4, median)
frollapply(1:9, 3, toString)

## vectorized input
x = list(1:10, 10:1)
n = c(3, 4)
frollapply(x, n, sum)
## give names
x = list(data1 = 1:10, data2 = 10:1)
n = c(small = 3, big = 4)
frollapply(x, n, sum, give.names=TRUE)

## by.column=FALSE
x = as.data.table(iris)
flow = function(x) {
  v1 = x[[1L]]
  v2 = x[[2L]]
  (v1[2L] - v1[1L] * (1+v2[2L])) / v1[1L]
}
x[, "flow" := frollapply(.(Sepal.Length, Sepal.Width), 2L, flow, by.column=FALSE),
  by = Species][]

## rolling regression: by.column=FALSE
f = function(x) coef(lm(v2 ~ v1, data=x))
x = data.table(v1=rnorm(120), v2=rnorm(120))
frollapply(x, 4, f, by.column=FALSE)
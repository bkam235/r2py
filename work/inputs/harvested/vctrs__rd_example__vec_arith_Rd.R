# r2py crawler metadata
# package: vctrs
# source_type: rd_example
# topic: vec_arith.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\help
# lines: 17

suppressPackageStartupMessages(library(vctrs))
d <- as.Date("2018-01-01")
dt <- as.POSIXct("2018-01-02 12:00")
t <- as.difftime(12, unit = "hours")

vec_arith("-", dt, 1)
vec_arith("-", dt, t)
vec_arith("-", dt, d)

vec_arith("+", dt, 86400)
vec_arith("+", dt, t)
vec_arith("+", t, t)

vec_arith("/", t, t)
vec_arith("/", t, 2)

vec_arith("*", t, 2)
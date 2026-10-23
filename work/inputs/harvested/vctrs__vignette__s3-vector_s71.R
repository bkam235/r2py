# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s71
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 25

suppressPackageStartupMessages(library(vctrs))
try({
vec_arith.vctrs_meter.numeric <- function(op, x, y, ...) {
  switch(
    op,
    "/" = ,
    "*" = new_meter(vec_arith_base(op, x, y)),
    stop_incompatible_op(op, x, y)
  )
}
vec_arith.numeric.vctrs_meter <- function(op, x, y, ...) {
  switch(
    op,
    "*" = new_meter(vec_arith_base(op, x, y)),
    stop_incompatible_op(op, x, y)
  )
}

meter(2) * 10
meter(2) * as.integer(10)
10 * meter(2)
meter(20) / 10
10 / meter(20)
meter(20) + 10
})
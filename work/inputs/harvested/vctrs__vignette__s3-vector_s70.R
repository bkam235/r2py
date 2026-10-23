# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s70
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 17

suppressPackageStartupMessages(library(vctrs))
try({
vec_arith.vctrs_meter.vctrs_meter <- function(op, x, y, ...) {
  switch(
    op,
    "+" = ,
    "-" = new_meter(vec_arith_base(op, x, y)),
    "/" = vec_arith_base(op, x, y),
    stop_incompatible_op(op, x, y)
  )
}

meter(10) + meter(1)
meter(10) - meter(1)
meter(10) / meter(1)
meter(10) * meter(1)
})
# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: s3-vector_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\s3-vector.R
# lines: 7

suppressPackageStartupMessages(library(vctrs))
format.vctrs_percent <- function(x, ...) {
  out <- formatC(signif(vec_data(x) * 100, 3))
  out[is.na(x)] <- NA
  out[!is.na(x)] <- paste0(out[!is.na(x)], "%")
  out
}
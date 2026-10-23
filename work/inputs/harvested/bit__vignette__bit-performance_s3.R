# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-performance_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-performance.R
# lines: 13

suppressPackageStartupMessages(library(bit))
# TODO(r-lib/lintr#773): nolint as a chunk option.
# nolint start: strings_as_factors_linter.
knitr::kable(
  data.frame(
    coin="random 50%",
    often="random 99%",
    rare="random 1%",
    chunk="contiguous chunk of 5%"
  ),
  caption="selection characteristic"
)
# nolint end: strings_as_factors_linter.
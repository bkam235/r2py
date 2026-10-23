# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-demo_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-demo.R
# lines: 6

knitr::opts_chunk$set(collapse = TRUE, comment = "#>")
library(bit)
.ff.is.available = requireNamespace("ff", quietly=TRUE) && packageVersion("ff") >= "4.0.0"
if (.ff.is.available) library(ff)
#tools::buildVignette("vignettes/bit-demo.Rmd")
#devtools::build_vignettes()
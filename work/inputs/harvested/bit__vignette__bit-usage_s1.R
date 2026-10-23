# r2py crawler metadata
# package: bit
# source_type: vignette
# topic: bit-usage_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bit\doc\bit-usage.R
# lines: 6

knitr::opts_chunk$set(collapse = TRUE, comment = "#>")
library(bit)
.ff.is.available = requireNamespace("ff", quietly=TRUE) && packageVersion("ff") >= "4.0.0"
if (.ff.is.available) library(ff)
# rmarkdown::render("vignettes/bit-usage.Rmd")
# devtools::build_vignettes()
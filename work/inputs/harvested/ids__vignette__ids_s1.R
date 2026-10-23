# r2py crawler metadata
# package: ids
# source_type: vignette
# topic: ids_s1
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ids\doc\ids.R
# lines: 15

suppressPackageStartupMessages(library(ids))
knitr::opts_chunk$set(error = FALSE)
human_no <- function(x) {
  s <- log10(floor(x + 1))
  p <- c(0, thousand = 3, million = 6, billion = 9, trillion = 12)
  i <- s > p
  j <- max(which(i))
  str <- names(p)[j]
  if (nzchar(str)) {
    paste(signif(x / 10^p[[j]], 3), str)
  } else {
    as.character(x)
  }
}
set.seed(1)
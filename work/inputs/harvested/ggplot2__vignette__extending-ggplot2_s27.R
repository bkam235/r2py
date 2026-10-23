# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s27
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 4

suppressPackageStartupMessages(library(ggplot2))
layout <- function(data, params) {
  data.frame(PANEL = c(1L, 2L), SCALE_X = 1L, SCALE_Y = 1L)
}
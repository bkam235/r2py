# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s28
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 10

suppressPackageStartupMessages(library(ggplot2))
mapping <- function(data, layout, params) {
  if (is.null(data) || nrow(data) == 0) {
    return(cbind(data, PANEL = integer(0)))
  }
  rbind(
    cbind(data, PANEL = 1L),
    cbind(data, PANEL = 2L)
  )
}
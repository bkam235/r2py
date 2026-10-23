# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 11

suppressPackageStartupMessages(library(vctrs))
deg <- function(x, direction) {
  pm <- if (direction == "lat") c("N", "S") else c("E", "W")

  sign <- sign(x)
  x <- abs(x)
  deg <- round(x)

  ret <- sprintf("%d°%s", deg, pm[ifelse(sign >= 0, 1, 2)])
  format(ret, justify = "right")
}
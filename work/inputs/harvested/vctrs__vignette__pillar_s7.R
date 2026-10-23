# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 19

suppressPackageStartupMessages(library(vctrs))
deg_min_color <- function(x, direction) {
  pm <- if (direction == "lat") c("N", "S") else c("E", "W")

  sign <- sign(x)
  x <- abs(x)
  deg <- trunc(x)
  x <- x - deg
  rad <- round(x * 60)
  ret <- sprintf(
    "%d%s%.2d%s%s",
    deg,
    pillar::style_subtle("°"),
    rad,
    pillar::style_subtle("'"),
    pm[ifelse(sign >= 0, 1, 2)]
  )
  format(ret, justify = "right")
}
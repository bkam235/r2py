# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 7

suppressPackageStartupMessages(library(vctrs))
#' @importFrom pillar pillar_shaft
#' @export
pillar_shaft.earth_latlon <- function(x, ...) {
  out <- format(x, formatter = deg_min_color)
  pillar::new_pillar_shaft_simple(out, align = "right")
}
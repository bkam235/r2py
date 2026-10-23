# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 14

suppressPackageStartupMessages(library(vctrs))
#' @importFrom pillar pillar_shaft
#' @export
pillar_shaft.earth_latlon <- function(x, ...) {
  deg <- format(x, formatter = deg)
  deg_min <- format(x)

  pillar::new_pillar_shaft(
    list(deg = deg, deg_min = deg_min),
    width = pillar::get_max_extent(deg_min),
    min_width = pillar::get_max_extent(deg),
    class = "pillar_shaft_latlon"
  )
}
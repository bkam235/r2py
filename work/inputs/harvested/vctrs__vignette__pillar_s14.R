# r2py crawler metadata
# package: vctrs
# source_type: vignette
# topic: pillar_s14
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\vctrs\doc\pillar.R
# lines: 14

suppressPackageStartupMessages(library(vctrs))
#' @export
format.pillar_shaft_latlon <- function(x, width, ...) {
  if (get_max_extent(x$deg_min) <= width) {
    ornament <- x$deg_min
  } else {
    ornament <- x$deg
  }

  pillar::new_ornament(ornament, align = "right")
}

data
print(data, width = 30)
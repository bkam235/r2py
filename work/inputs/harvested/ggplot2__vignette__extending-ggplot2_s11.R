# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: extending-ggplot2_s11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\extending-ggplot2.R
# lines: 16

suppressPackageStartupMessages(library(ggplot2))
#' @export
#' @inheritParams ggplot2::stat_identity
#' @param formula The modelling formula passed to \code{lm}. Should only 
#'   involve \code{y} and \code{x}
#' @param n Number of points used for interpolation.
stat_lm <- function(mapping = NULL, data = NULL, geom = "line",
                    position = "identity", na.rm = FALSE, show.legend = NA, 
                    inherit.aes = TRUE, n = 50, formula = y ~ x, 
                    ...) {
  layer(
    stat = StatLm, data = data, mapping = mapping, geom = geom, 
    position = position, show.legend = show.legend, inherit.aes = inherit.aes,
    params = list(n = n, formula = formula, na.rm = na.rm, ...)
  )
}
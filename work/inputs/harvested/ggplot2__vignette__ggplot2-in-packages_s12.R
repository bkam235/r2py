# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s12
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 9

suppressPackageStartupMessages(library(ggplot2))
#' @importFrom ggplot2 autoplot
autoplot.discrete_distr <- function(object, ...) {
  plot_data <- discrete_distr_data(object)
  ggplot(plot_data, aes(.data$value, .data$probability)) +
    geom_col() +
    coord_flip() +
    labs(x = "Value", y = "Probability")
}
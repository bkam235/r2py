# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s13
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 5

suppressPackageStartupMessages(library(ggplot2))
#' @importFrom graphics plot
plot.discrete_distr <- function(x, ...) {
  print(autoplot(x, ...))
}
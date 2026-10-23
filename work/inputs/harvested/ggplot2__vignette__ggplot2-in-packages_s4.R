# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 7

suppressPackageStartupMessages(library(ggplot2))
#' @importFrom ggplot2 ggplot aes geom_bar coord_flip
mpg_drv_summary <- function() {
  ggplot(ggplot2::mpg) + 
    geom_bar(aes(x = drv)) + 
    coord_flip()
}
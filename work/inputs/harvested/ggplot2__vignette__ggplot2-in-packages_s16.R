# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s16
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 7

suppressPackageStartupMessages(library(ggplot2))
theme_custom <- function(...) {
  `%+replace%` <- ggplot2::`%+replace%`
  
  ggplot2::theme_grey(...) %+replace% 
    ggplot2::theme(panel.background = ggplot2::element_blank())
}
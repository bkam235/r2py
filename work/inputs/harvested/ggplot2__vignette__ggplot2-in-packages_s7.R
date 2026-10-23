# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s7
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 6

suppressPackageStartupMessages(library(ggplot2))
mpg_drv_summary <- function() {
  ggplot(ggplot2::mpg) + 
    geom_bar(aes(y = .data$drv)) +
    facet_wrap(vars(.data$year))
}
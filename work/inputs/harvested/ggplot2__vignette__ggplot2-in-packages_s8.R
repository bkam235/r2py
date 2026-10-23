# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s8
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 8

suppressPackageStartupMessages(library(ggplot2))
col_summary <- function(df, col, by) {
  ggplot(df) + 
    geom_bar(aes(y = .data[[col]])) + 
    facet_wrap(vars(.data[[by]]))
}

col_summary(mpg, "drv", "year")
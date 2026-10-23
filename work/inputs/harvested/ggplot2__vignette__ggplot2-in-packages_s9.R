# r2py crawler metadata
# package: ggplot2
# source_type: vignette
# topic: ggplot2-in-packages_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\ggplot2\doc\ggplot2-in-packages.R
# lines: 9

suppressPackageStartupMessages(library(ggplot2))
#| eval: !expr (packageVersion("rlang") >= "0.3.4.9003")
col_summary <- function(df, col, by) {
  ggplot(df) + 
    geom_bar(aes(y = {{ col }})) + 
    facet_wrap(vars({{ by }}))
}

col_summary(mpg, drv, year)
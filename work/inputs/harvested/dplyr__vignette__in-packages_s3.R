# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: in-packages_s3
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\in-packages.R
# lines: 8

suppressPackageStartupMessages(library(dplyr))
my_summary_function <- function(data) {
  data |>
    select(grp, x, y) |>
    filter(x > 0) |>
    group_by(grp) |>
    summarise(y = mean(y), n = n())
}
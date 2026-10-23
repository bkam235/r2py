# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: in-packages_s4
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\in-packages.R
# lines: 9

suppressPackageStartupMessages(library(dplyr))
#' @importFrom rlang .data
my_summary_function <- function(data) {
  data |>
    select("grp", "x", "y") |>
    filter(.data$x > 0) |>
    group_by(.data$grp) |>
    summarise(y = mean(.data$y), n = n())
}
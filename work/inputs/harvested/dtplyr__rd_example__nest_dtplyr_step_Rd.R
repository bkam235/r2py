# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: nest.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 7

suppressPackageStartupMessages(library(dtplyr))
if (require("tidyr", quietly = TRUE)) {
  dt <- lazy_dt(tibble(x = c(1, 2, 1), y = c("a", "a", "b")))
  dt %>% nest(data = y)

  dt %>% dplyr::group_by(x) %>% nest()
}
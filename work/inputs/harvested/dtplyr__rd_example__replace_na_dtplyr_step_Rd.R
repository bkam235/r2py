# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: replace_na.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 9

suppressPackageStartupMessages(library(dtplyr))
library(tidyr)

# Replace NAs in a data frame
dt <- lazy_dt(tibble(x = c(1, 2, NA), y = c("a", NA, "b")))
dt %>% replace_na(list(x = 0, y = "unknown"))

# Replace NAs using `dplyr::mutate()`
dt %>% dplyr::mutate(x = replace_na(x, 0))
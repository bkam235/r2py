# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: select.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 8

suppressPackageStartupMessages(library(dtplyr))
library(dplyr, warn.conflicts = FALSE)

dt <- lazy_dt(data.frame(x1 = 1, x2 = 2, y1 = 3, y2 = 4))

dt %>% select(starts_with("x"))
dt %>% select(ends_with("2"))
dt %>% select(z1 = x1, z2 = x2)
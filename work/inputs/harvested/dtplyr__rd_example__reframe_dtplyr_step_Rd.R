# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: reframe.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 14

suppressPackageStartupMessages(library(dtplyr))
library(dplyr, warn.conflicts = FALSE)

dt <- lazy_dt(mtcars)

dt %>%
  reframe(qs = quantile(disp, c(0.25, 0.75)),
          prob = c(0.25, 0.75),
          .by = cyl)

dt %>%
  group_by(cyl) %>%
  reframe(qs = quantile(disp, c(0.25, 0.75)),
          prob = c(0.25, 0.75))
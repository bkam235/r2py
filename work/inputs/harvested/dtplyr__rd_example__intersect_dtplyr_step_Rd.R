# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: intersect.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 7

suppressPackageStartupMessages(library(dtplyr))
dt1 <- lazy_dt(data.frame(x = 1:4))
dt2 <- lazy_dt(data.frame(x = c(2, 4, 6)))

intersect(dt1, dt2)
union(dt1, dt2)
setdiff(dt1, dt2)
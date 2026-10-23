# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: group_by.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 15

suppressPackageStartupMessages(library(dtplyr))
library(dplyr, warn.conflicts = FALSE)
dt <- lazy_dt(mtcars)

# group_by() is usually translated to `keyby` so that the groups
# are ordered in the output
dt %>%
 group_by(cyl) %>%
 summarise(mpg = mean(mpg))

# use `arrange = FALSE` to instead use `by` so the original order
# or groups is preserved
dt %>%
 group_by(cyl, arrange = FALSE) %>%
 summarise(mpg = mean(mpg))
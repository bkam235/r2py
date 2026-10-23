# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: collect.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 24

suppressPackageStartupMessages(library(dtplyr))
library(dplyr, warn.conflicts = FALSE)

dt <- lazy_dt(mtcars)

# Generate translation
avg_mpg <- dt %>%
  filter(am == 1) %>%
  group_by(cyl) %>%
  summarise(mpg = mean(mpg))

# Show translation and temporarily compute result
avg_mpg

# compute and return tibble
avg_mpg_tb <- as_tibble(avg_mpg)
avg_mpg_tb

# compute and return data.table
avg_mpg_dt <- data.table::as.data.table(avg_mpg)
avg_mpg_dt

# modify translation to use intermediate assignment
compute(avg_mpg)
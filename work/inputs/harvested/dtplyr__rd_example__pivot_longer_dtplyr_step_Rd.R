# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: pivot_longer.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 37

suppressPackageStartupMessages(library(dtplyr))
library(tidyr)

# Simplest case where column names are character data
relig_income_dt <- lazy_dt(relig_income)
relig_income_dt %>%
  pivot_longer(!religion, names_to = "income", values_to = "count")

# Slightly more complex case where columns have common prefix,
# and missing missings are structural so should be dropped.
billboard_dt <- lazy_dt(billboard)
billboard %>%
 pivot_longer(
   cols = starts_with("wk"),
   names_to = "week",
   names_prefix = "wk",
   values_to = "rank",
   values_drop_na = TRUE
 )

# Multiple variables stored in column names
lazy_dt(who) %>%
  pivot_longer(
    cols = new_sp_m014:newrel_f65,
    names_to = c("diagnosis", "gender", "age"),
    names_pattern = "new_?(.*)_(.)(.*)",
    values_to = "count"
  )

# Multiple observations per row
anscombe_dt <- lazy_dt(anscombe)
anscombe_dt %>%
 pivot_longer(
   everything(),
   names_to = c(".value", "set"),
   names_pattern = "(.)(.)"
 )
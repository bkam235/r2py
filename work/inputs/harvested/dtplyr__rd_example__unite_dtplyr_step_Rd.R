# r2py crawler metadata
# package: dtplyr
# source_type: rd_example
# topic: unite.dtplyr_step.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dtplyr\help
# lines: 13

suppressPackageStartupMessages(library(dtplyr))
library(tidyr)

df <- lazy_dt(expand_grid(x = c("a", NA), y = c("b", NA)))
df

df %>% unite("z", x:y, remove = FALSE)

# Separate is almost the complement of unite
df %>%
  unite("xy", x:y) %>%
  separate(xy, c("x", "y"))
# (but note `x` and `y` contain now "NA" not NA)
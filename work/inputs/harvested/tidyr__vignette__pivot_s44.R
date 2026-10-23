# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_s44
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.R
# lines: 8

suppressPackageStartupMessages(library(tidyr))
pop2 <- world_bank_pop |>
  pivot_longer(
    cols = `2000`:`2017`,
    names_to = "year",
    values_to = "value"
  )
pop2
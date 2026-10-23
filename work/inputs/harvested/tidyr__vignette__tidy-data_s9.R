# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: tidy-data_s9
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\tidy-data.R
# lines: 9

suppressPackageStartupMessages(library(tidyr))
billboard2 <- billboard |>
  pivot_longer(
    wk1:wk76,
    names_to = "week",
    values_to = "rank",
    values_drop_na = TRUE
  )
billboard2
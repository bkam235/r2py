# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s6
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 13

suppressPackageStartupMessages(library(dplyr))
try({
racers |>
  mutate(
    tier = case_when(
      time < 23 ~ "A",
      time < 27 ~ "B",
      time < 30 ~ "C",
      time < 33 ~ "D",
      .unmatched = "error"
    )
  )
})
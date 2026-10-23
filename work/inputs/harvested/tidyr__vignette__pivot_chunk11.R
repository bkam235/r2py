# r2py crawler metadata
# package: tidyr
# source_type: vignette
# topic: pivot_chunk11
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\tidyr\doc\pivot.Rmd
# lines: 16

suppressPackageStartupMessages(library(tidyr))
who |>
  pivot_longer(
    cols = new_sp_m014:newrel_f65,
    names_to = c("diagnosis", "gender", "age"),
    names_pattern = "new_?(.*)_(.)(.*)",
    names_transform = list(
      gender = ~ readr::parse_factor(.x, levels = c("f", "m")),
      age = ~ readr::parse_factor(
        .x,
        levels = c("014", "1524", "2534", "3544", "4554", "5564", "65"),
        ordered = TRUE
      )
    ),
    values_to = "count",
)
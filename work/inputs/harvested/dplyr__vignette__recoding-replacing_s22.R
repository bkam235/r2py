# r2py crawler metadata
# package: dplyr
# source_type: vignette
# topic: recoding-replacing_s22
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\dplyr\doc\recoding-replacing.R
# lines: 17

suppressPackageStartupMessages(library(dplyr))
try({
likert <- tibble(
  score = c(0, 1, 2, 2, 4, 5, 2, 3, 1, 4)
)

# Missed the `0`
likert |>
  mutate(
    score = score |>
      recode_values(
        from = lookup$from,
        to = lookup$to,
        unmatched = "error"
      )
  )
})
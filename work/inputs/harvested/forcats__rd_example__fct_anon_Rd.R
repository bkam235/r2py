# r2py crawler metadata
# package: forcats
# source_type: rd_example
# topic: fct_anon.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\forcats\help
# lines: 8

suppressPackageStartupMessages(library(forcats))
gss_cat$relig |> fct_count()
gss_cat$relig |>
  fct_anon() |>
  fct_count()
gss_cat$relig |>
  fct_anon("X") |>
  fct_count()
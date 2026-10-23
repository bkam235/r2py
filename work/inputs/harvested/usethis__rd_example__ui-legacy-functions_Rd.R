# r2py crawler metadata
# package: usethis
# source_type: rd_example
# topic: ui-legacy-functions.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\usethis\help
# lines: 10

suppressPackageStartupMessages(library(usethis))
new_val <- "oxnard"
ui_done("{ui_field('name')} set to {ui_value(new_val)}")
ui_todo("Redocument with {ui_code('devtools::document()')}")

ui_code_block(c(
  "Line 1",
  "Line 2",
  "Line 3"
))
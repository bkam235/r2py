# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: value_box.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 15

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(htmltools)

value_box(
  "KPI Title",
  h1(HTML("$1 <i>Billion</i> Dollars")),
  span(
    bsicons::bs_icon("arrow-up"),
    " 30% VS PREVIOUS 30 DAYS"
  ),
  showcase = bsicons::bs_icon("piggy-bank"),
  theme = "success"
)
}) # examplesIf
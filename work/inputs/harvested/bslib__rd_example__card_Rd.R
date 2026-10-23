# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: card.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 18

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
library(htmltools)

card(
  full_screen = TRUE,
  card_header(
    "This is the header"
  ),
  card_body(
    p("This is the body."),
    p("This is still the body.")
  ),
  card_footer(
    "This is the footer"
  )
)
}) # examplesIf
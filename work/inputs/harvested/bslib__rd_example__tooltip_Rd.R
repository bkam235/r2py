# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: tooltip.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 19

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf

tooltip(
  shiny::actionButton("btn", "A button"),
  "A message"
)

card(
  card_header(
    tooltip(
      span("Card title ", bsicons::bs_icon("question-circle-fill")),
      "Additional info",
      placement = "right"
    )
  ),
  "Card body content..."
)
}) # examplesIf
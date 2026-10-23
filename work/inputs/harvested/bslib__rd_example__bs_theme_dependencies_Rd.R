# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bs_theme_dependencies.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 19

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf

# Function to preview the styling a (primary) Bootstrap button
library(htmltools)
button <- tags$a(class = "btn btn-primary", href = "#", role = "button", "Hello")
preview_button <- function(theme) {
  browsable(tags$body(bs_theme_dependencies(theme), button))
}

# Latest Bootstrap
preview_button(bs_theme())
# Bootstrap 3
preview_button(bs_theme(3))
# Bootswatch 4 minty theme
preview_button(bs_theme(4, bootswatch = "minty"))
# Bootswatch 4 sketchy theme
preview_button(bs_theme(4, bootswatch = "sketchy"))
}) # examplesIf
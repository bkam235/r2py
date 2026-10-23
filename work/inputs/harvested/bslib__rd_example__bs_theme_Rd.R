# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bs_theme.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 22

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf

theme <- bs_theme(
  # Controls the default grayscale palette
  bg = "#202123", fg = "#B8BCC2",
  # Controls the accent (e.g., hyperlink, button, etc) colors
  primary = "#EA80FC", secondary = "#48DAC6",
  base_font = c("Grandstander", "sans-serif"),
  code_font = c("Courier", "monospace"),
  heading_font = "'Helvetica Neue', Helvetica, sans-serif",
  # Can also add lower-level customization
  "input-border-color" = "#EA80FC"
)

bs_theme_preview(theme)

# Lower-level bs_add_*() functions allow you to work more
# directly with the underlying Sass code
theme <- bs_add_variables(theme, "my-class-color" = "red")
theme <- bs_add_rules(theme, ".my-class { color: $my-class-color }")
}) # examplesIf
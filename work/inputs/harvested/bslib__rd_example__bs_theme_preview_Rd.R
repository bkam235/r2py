# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bs_theme_preview.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 5

suppressPackageStartupMessages(library(bslib))
if (rlang::is_interactive()) withAutoprint({ # examplesIf
theme <- bs_theme(bg = "#6c757d", fg = "white", primary = "orange")
bs_theme_preview(theme)
}) # examplesIf
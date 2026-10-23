# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bs_global_theme.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 16

suppressPackageStartupMessages(library(bslib))
# Remember the global state now (so we can restore later)
theme <- bs_global_get()

# Use Bootstrap 3 (globally) with some theme customization
bs_global_theme(3, bg = "#444", fg = "#e4e4e4", primary = "#e39777")
if (rlang::is_interactive()) {
  bs_theme_preview(with_themer = FALSE)
}

# If no global theme is active, bs_global_get() returns NULL
bs_global_clear()
bs_global_get()

# Restore the original state
bs_global_set(theme)
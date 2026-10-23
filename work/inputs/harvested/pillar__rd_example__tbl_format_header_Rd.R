# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: tbl_format_header.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 8

suppressPackageStartupMessages(library(pillar))
if (rlang::is_installed(c("palmerpenguins", "tibble"))) withAutoprint({ # examplesIf
setup <- tbl_format_setup(palmerpenguins::penguins)
tbl_format_header(palmerpenguins::penguins, setup)

# Shortcut for debugging
tbl_format_header(setup)
}) # examplesIf
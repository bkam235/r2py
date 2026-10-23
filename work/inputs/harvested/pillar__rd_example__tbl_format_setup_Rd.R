# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: tbl_format_setup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 4

suppressPackageStartupMessages(library(pillar))
if (rlang::is_installed(c("palmerpenguins", "tibble"))) withAutoprint({ # examplesIf
tbl_format_setup(palmerpenguins::penguins)
}) # examplesIf
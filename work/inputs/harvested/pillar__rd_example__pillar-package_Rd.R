# r2py crawler metadata
# package: pillar
# source_type: rd_example
# topic: pillar-package.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\pillar\help
# lines: 7

suppressPackageStartupMessages(library(pillar))
if (rlang::is_installed("tibble")) withAutoprint({ # examplesIf
pillar(1:3)
pillar(c(1, 2, 3))
pillar(factor(letters[1:3]), title = "letters")
tbl_format_setup(tibble::as_tibble(mtcars), width = 60)
}) # examplesIf
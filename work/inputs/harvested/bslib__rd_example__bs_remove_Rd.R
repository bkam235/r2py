# r2py crawler metadata
# package: bslib
# source_type: rd_example
# topic: bs_remove.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\bslib\help
# lines: 14

suppressPackageStartupMessages(library(bslib))
bs4 <- bs_theme(version = 4)

# Retrieve sass bundle for print styles
bs_retrieve(bs4, "_print", include_unnamed = FALSE)

# Remove CSS rules for print and carousels
bs4_no_print <- bs_remove(bs4, c("_print", "_carousel"))
suppressWarnings(
  bs_retrieve(bs4_no_print, "_print", include_unnamed = FALSE)
)

# Remove BS3 compatibility layer
bs4_no_compat <- bs_remove(bs4, "bs3compat")
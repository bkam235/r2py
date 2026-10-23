# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: system_fonts.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 4

suppressPackageStartupMessages(library(systemfonts))
# See all monospace fonts
fonts <- system_fonts()
fonts[fonts$monospace, ]
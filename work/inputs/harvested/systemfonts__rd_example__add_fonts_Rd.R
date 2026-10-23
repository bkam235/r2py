# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: add_fonts.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 7

suppressPackageStartupMessages(library(systemfonts))
# example code
empty_font <- system.file("unfont.ttf", package = "systemfonts")

add_fonts(empty_font)

clear_local_fonts()
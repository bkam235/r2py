# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: font_info.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 6

suppressPackageStartupMessages(library(systemfonts))
font_info('serif')

# Avoid lookup if font file is already known
sans <- match_fonts('sans')
font_info(path = sans$path, index = sans$index)
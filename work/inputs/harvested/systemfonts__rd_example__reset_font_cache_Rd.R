# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: reset_font_cache.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 14

suppressPackageStartupMessages(library(systemfonts))
all_fonts <- system_fonts()

##-- Install a new font on the system --##

all_fonts_new <- system_fonts()

## all_fonts_new will be equal to all_fonts

reset_font_cache()

all_fonts_new <- system_fonts()

## all_fonts_new will now contain the new font
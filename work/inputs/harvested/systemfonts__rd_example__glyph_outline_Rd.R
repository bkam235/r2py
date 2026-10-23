# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: glyph_outline.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 8

suppressPackageStartupMessages(library(systemfonts))
# Get the shape of s in the default font
font <- font_info()
glyph <- glyph_info("s", path = font$path, index = font$index)

s <- glyph_outline(glyph$index, font$path, font$index, size = 150)

plot(s$x, s$y, type = 'l')
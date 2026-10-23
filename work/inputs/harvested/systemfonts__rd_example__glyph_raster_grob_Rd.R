# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: glyph_raster_grob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 13

suppressPackageStartupMessages(library(systemfonts))
font <- font_info()
glyph <- glyph_info("R", path = font$path, index = font$index)

R <- glyph_raster(glyph$index, font$path, font$index, size = 150)

grob <- glyph_raster_grob(R[[1]], 50, 50)

grid::grid.newpage()
# Mark the baseline location
grid::grid.points(50, 50, default.units = "bigpts")
# Draw the glyph
grid::grid.draw(grob)
# r2py crawler metadata
# package: systemfonts
# source_type: rd_example
# topic: glyph_raster.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\systemfonts\help
# lines: 9

suppressPackageStartupMessages(library(systemfonts))
font <- font_info()
glyph <- glyph_info("R", path = font$path, index = font$index)

R <- glyph_raster(glyph$index, font$path, font$index, size = 150)

plot.new()
plot.window(c(0,150), c(0, 150), asp = 1)
rasterImage(R[[1]], 0, 0, attr(R[[1]], "size")[2], attr(R[[1]], "size")[1])
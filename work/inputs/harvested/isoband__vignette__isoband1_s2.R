# r2py crawler metadata
# package: isoband
# source_type: vignette
# topic: isoband1_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\doc\isoband1.R
# lines: 21

library(isoband)
library(grid)

m <- matrix(
  c(0, 0, 0, 0, 0,
    0, 1, 2, 1, 0,
    0, 1, 2, 0, 0,
    0, 1, 0, 1, 0,
    0, 0, 0, 0, 0),
  5, 5, byrow = TRUE
)

lines <- isolines(x = 1:ncol(m)/6, y = nrow(m):1/6, z = m, levels = 0.5)
lines
grid.newpage()
grid.draw(polylineGrob(lines[[1]]$x, lines[[1]]$y, lines[[1]]$id))

bands <- isobands(x = 1:ncol(m)/6, y = nrow(m):1/6, z = m, levels_low = 0.5, levels_high = 1.5)
bands
grid.newpage()
grid.draw(pathGrob(bands[[1]]$x, bands[[1]]$y, bands[[1]]$id, gp = gpar(fill = "cornsilk")))
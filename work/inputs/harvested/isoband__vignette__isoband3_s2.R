# r2py crawler metadata
# package: isoband
# source_type: vignette
# topic: isoband3_s2
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\doc\isoband3.R
# lines: 18

library(isoband)
library(grid)

x <- (0:(ncol(volcano) - 1))/(ncol(volcano) - 1)
y <- ((nrow(volcano) - 1):0)/(nrow(volcano) - 1)
lines <- isolines(x, y, volcano, 5*(19:38))

g <- isolines_grob(
  lines, breaks = 20*(5:10),
  gp = gpar(
    fontsize = 10,
    lwd = c(1, 2, 1, 1),
    col = c("grey50", "grey20", "grey50", "grey50")
  )
)

grid.newpage()
grid.draw(g)
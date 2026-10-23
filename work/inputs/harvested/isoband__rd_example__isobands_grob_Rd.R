# r2py crawler metadata
# package: isoband
# source_type: rd_example
# topic: isobands_grob.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\isoband\help
# lines: 19

suppressPackageStartupMessages(library(isoband))
library(grid)

viridis_pal <- colorRampPalette(
  c("#440154", "#414487", "#2A788E", "#22A884", "#7AD151", "#FDE725"),
  space = "Lab"
)

x <- (1:ncol(volcano))/(ncol(volcano)+1)
y <- (nrow(volcano):1)/(nrow(volcano)+1)
bands <- isobands(x, y, volcano, 5*(18:38), 5*(19:39))

b <- isobands_grob(
  bands,
  gp = gpar(col = "black", fill = viridis_pal(21), alpha = 0.5)
)

grid.newpage()
grid.draw(b)
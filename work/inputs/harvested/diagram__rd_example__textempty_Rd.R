# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: textempty.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 8

suppressPackageStartupMessages(library(diagram))
openplotmat(xlim = c(-0.1, 1.1), col = "lightgrey", main = "textempty")

for (i in 1:10) 
  textempty(mid = runif(2), box.col = i, lab = LETTERS[i], cex = 2)

textempty(mid = c(0.5, 0.5), adj = c(0, 0), 
  lab = "textempty", box.col = "white")
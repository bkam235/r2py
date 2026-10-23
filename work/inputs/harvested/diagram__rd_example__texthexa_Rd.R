# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: texthexa.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 7

suppressPackageStartupMessages(library(diagram))
openplotmat(xlim = c(-0.1, 1.1), main = "texthexa")

  for (i in 1:20) 
    texthexa(mid = runif(2), angle = runif(1)*360, col = i,
             box.col = grey(0.95), radx = 0.1, rady = 0.05,
             lab = LETTERS[i], cex = 2)
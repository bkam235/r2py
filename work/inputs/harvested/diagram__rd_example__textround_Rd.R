# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: textround.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 7

suppressPackageStartupMessages(library(diagram))
openplotmat(xlim = c(-0.1, 1.1), main = "textround")

  for (i in 1:10) 
    textround(mid = runif(2), col = i, 
              radx = 0.03, rady = 0.075,
              lab = LETTERS[i], cex = 2)
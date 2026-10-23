# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: textmulti.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 6

suppressPackageStartupMessages(library(diagram))
openplotmat(xlim = c(-0.1, 1.1), main = "textmulti")

  for (i in 1:10) 
    textmulti(mid = runif(2), col = i, radx = 0.1, rady = 0.1,
             lab = LETTERS[i], cex = 2, nr = trunc(i/1.5)+3)
# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: roundrect.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 7

suppressPackageStartupMessages(library(shape))
emptyplot(c(-0.1, 1.1), main = "roundrect")
for (i in 1:10) 
  roundrect(mid = runif(2), col = i, radx = 0.1, rady = 0.05)
for (i in 1:5)
  roundrect(mid = runif(2), col = greycol(20), radx = 0.05,
            rady = 0.05, angle = runif(1)*360)
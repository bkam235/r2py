# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: coordinates.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 14

suppressPackageStartupMessages(library(diagram))
openplotmat(main = "coordinates")

text(coordinates(N = 6), lab = LETTERS[1:6], cex = 2)

text(coordinates(N = 8, relsize = 0.5), lab = letters[1:8], cex = 2)

openplotmat(main = "coordinates")

text(coordinates(pos = c(2, 4, 2)), lab = letters[1:8], cex = 2)

plot(0, type = "n", xlim = c(0, 5), ylim = c(2, 8), main = "coordinates")

text(coordinates(pos = c(2, 4, 3), hor = FALSE), lab = 1:9, cex = 2)
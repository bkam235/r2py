# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: selfarrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 18

suppressPackageStartupMessages(library(diagram))
openplotmat(main = "selfarrow")

pos <- coordinates(3, mx = 0.05)

text(pos, LETTERS[1:3], cex = 2)

for (i in 1:3) 
  selfarrow(pos = pos[i, ], path = "R", arr.pos = 0.2,
            curve = c(0.05, 0.1), lcol = "darkred")

for (i in 1:3) 
  selfarrow(pos = pos[i, ], path = "L", arr.pos = 0.7,
            lcol = "darkblue", curve = c(0.05, 0.05))

for (i in 1:3) 
  selfarrow(pos = pos[i, ], path = "L", arr.pos = 0.5,
            lcol = "darkgreen", code = i, arr.type = "triangle")
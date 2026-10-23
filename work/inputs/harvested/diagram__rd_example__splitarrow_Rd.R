# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: splitarrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 25

suppressPackageStartupMessages(library(diagram))
openplotmat(main = "splitarrow")

pos <- coordinates(c(1, 2, 2, 4, 1))
splitarrow(from = pos[1, ], to = pos[2:10, ], 
           arr.side = 1, centre = c(0.5, 0.625))
for (i in 1:10) 
  textrect(pos[i, ], lab = i, cex = 2, radx = 0.05)
  
  
openplotmat(main = "splitarrow")

pos <- coordinates(c(1, 3))
splitarrow(from = pos[1,], to = pos[2:4, ], arr.side = 1)
splitarrow(from = pos[1,], to = pos[2:4, ], arr.side = 2)
for (i in 1:4) 
  textrect(pos[i, ], lab = i, cex = 2, radx = 0.05)
  

openplotmat(main = "splitarrow")
pos <- coordinates(N = 6)
pos <- rbind(c(0.5, 0.5), pos)
splitarrow(from = pos[1, ], to = pos[2:7, ], arr.side = 2)
for (i in 1:7)
  textrect(pos[i, ], lab = i, cex = 2, radx = 0.05)
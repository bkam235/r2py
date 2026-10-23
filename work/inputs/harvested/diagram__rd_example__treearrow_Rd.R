# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: treearrow.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 19

suppressPackageStartupMessages(library(diagram))
openplotmat(main = "treearrow")
pos <- coordinates(c(3, 2, 4, 1))
treearrow(from = pos[1:5, ], to = pos[6:10, ])
for (i in 1:10) 
  textrect(pos[i, ], lab = i, cex = 2, radx = 0.05)
  
openplotmat(main = "treearrow")
pos <- coordinates(c(2, 4), hor = FALSE)
treearrow(from = pos[1:2, ], to = pos[3:6, ], 
          arr.side = 1:2, path = "V")
for (i in 1:6) 
  textrect(pos[i, ], lab = i, cex = 2, radx = 0.05)
  
openplotmat(main = "treearrow")
pos <- coordinates(c(3, 5, 7, 7, 5, 3))
treearrow(from = pos[1:15, ], to = pos[15:30, ], arr.side = 0)
for (i in 1:30) 
  textrect(pos[i, ], lab = i, cex = 1.2, radx = 0.025)
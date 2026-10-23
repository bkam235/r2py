# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: shadowbox.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 15

suppressPackageStartupMessages(library(diagram))
openplotmat(main="shadowbox")

shadowbox(box.type = "rect", mid = c(0.1, 0.5),
          rady = 0.1, radx = 0.05, angle = 25)

shadowbox(box.type = "round", mid = c(0.3, 0.5),
          rady = 0.05, radx = 0.025, angle = 90,
          shadow.col = "darkred")

shadowbox(box.type = "ellipse", mid = c(0.5, 0.5),
          rady = 0.05, radx = 0.075, box.col = "blue")
          
shadowbox(box.type = "multi", mid = c(0.8, 0.5),
          rady = 0.05, radx = 0.05, box.col = "darkblue", nr = 5)
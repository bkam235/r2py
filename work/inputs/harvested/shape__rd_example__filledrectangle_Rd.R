# r2py crawler metadata
# package: shape
# source_type: rd_example
# topic: filledrectangle.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\shape\help
# lines: 22

suppressPackageStartupMessages(library(shape))
color <- shadepalette(grey(0.3), "lightblue", n = 50)
emptyplot(main = "filledrectangle")
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(0.5, 0.5), angle = 0)
filledrectangle(wx = 0.25, wy = 0.25, col = "darkblue", 
                mid = c(0.5, 0.5), angle = 45)
filledrectangle(wx = 0.125, wy = 0.125, col = c("lightblue","blue"),
                mid = c(0.5, 0.5), angle = 90)
  
color <- shadepalette(grey(0.3), "blue", n = 50)
emptyplot(c(-1, 1), main = "filledrectangle")
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(0, 0), angle = 0)
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(0.5, 0.5), angle = 90)
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(-0.5, -0.5), angle = -90)
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(0.5, -0.5), angle = 180)
filledrectangle(wx = 0.5, wy = 0.5, col = color, 
                mid = c(-0.5, 0.5), angle = 270)
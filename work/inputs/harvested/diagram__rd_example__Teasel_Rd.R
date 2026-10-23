# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: Teasel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 12

suppressPackageStartupMessages(library(diagram))
curves <- matrix(nrow = ncol(Teasel), ncol = ncol(Teasel), 0)
curves[3,1] <- curves[1,6] <- -0.35
curves[4,6] <- curves[6,4] <- curves[5,6] <- curves[6,5] <- 0.08
curves[3,6] <- 0.35
  
plotmat(Teasel, pos = c(3, 2, 1), curve = curves, lwd = 1, box.lwd = 2,
        cex.txt = 0.8, box.cex = 0.8, box.size = 0.08, arr.length = 0.5,
        box.type = "circle", box.prop = 1, shadow.size = 0.01,
        self.cex = 0.6, my = -0.075, mx = -0.01, relsize = 0.9,
        self.shifty = 0, self.shiftx = c(0, 0, 0.125, -0.12, 0.125, 0),
        main = "Dispsacus sylvestris")
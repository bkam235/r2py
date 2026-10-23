# r2py crawler metadata
# package: diagram
# source_type: rd_example
# topic: plotweb.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\diagram\help
# lines: 12

suppressPackageStartupMessages(library(diagram))
plotweb(Rigaweb, main = "Gulf of Riga food web",
        sub = "mgC/m3/d", val = TRUE)

ArrCol <- Rigaweb
ArrCol[] <- "black"
ArrCol[,"Sedimentation"] <- "green"

plotweb(Rigaweb, main = "Gulf of Riga food web",
        sub = "mgC/m3/d", val = FALSE, arr.col = ArrCol)

plotweb(diag(20), main = "plotweb")
# r2py crawler metadata
# package: prodlim
# source_type: rd_example
# topic: plotIllnessDeathModel.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\prodlim\help
# lines: 8

suppressPackageStartupMessages(library(prodlim))
plotIllnessDeathModel()
plotIllnessDeathModel(style=2)
plotIllnessDeathModel(style=2,
                      stateLabels=c("a","b\nc","d"),
                      box1.col="yellow",
                      box2.col="green",
                      box3.col="red")
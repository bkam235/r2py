# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: avNNet.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 7

suppressPackageStartupMessages(library(caret))
data(BloodBrain)

modelFit <- avNNet(bbbDescr, logBBB, size = 5, linout = TRUE, trace = FALSE)
modelFit

predict(modelFit, bbbDescr)
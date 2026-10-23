# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: preProcess.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 9

suppressPackageStartupMessages(library(caret))
data(BloodBrain)
# one variable has one unique value

preProc <- preProcess(bbbDescr)

preProc  <- preProcess(bbbDescr[1:100,-3])
training <- predict(preProc, bbbDescr[1:100,-3])
test     <- predict(preProc, bbbDescr[101:208,-3])
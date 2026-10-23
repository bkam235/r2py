# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: filterVarImp.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 13

suppressPackageStartupMessages(library(caret))
data(mdrr)
filterVarImp(mdrrDescr[, 1:5], mdrrClass)

data(BloodBrain)

filterVarImp(bbbDescr[, 1:5], logBBB, nonpara = FALSE)
apply(bbbDescr[, 1:5],
      2,
      function(x, y) summary(lm(y~x))$coefficients[2,3],
      y = logBBB)

filterVarImp(bbbDescr[, 1:5], logBBB, nonpara = TRUE)
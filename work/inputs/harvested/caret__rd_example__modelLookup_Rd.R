# r2py crawler metadata
# package: caret
# source_type: rd_example
# topic: modelLookup.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\caret\help
# lines: 9

suppressPackageStartupMessages(library(caret))
modelLookup()
modelLookup("gbm")

getModelInfo("pls")
getModelInfo("^pls")
getModelInfo("pls", regex = FALSE)

checkInstall(getModelInfo("pls")$library)
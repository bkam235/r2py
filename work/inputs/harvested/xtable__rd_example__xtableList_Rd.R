# r2py crawler metadata
# package: xtable
# source_type: rd_example
# topic: xtableList.Rd
# source_file: C:\Users\bened\AppData\Local\R\win-library\4.5\xtable\help
# lines: 11

suppressPackageStartupMessages(library(xtable))
data(mtcars)
mtcars <- mtcars[, 1:6]
mtcarsList <- split(mtcars, f = mtcars$cyl)
attr(mtcarsList, "subheadings") <- paste0("Number of cylinders = ",
                                          names(mtcarsList))
attr(mtcarsList, "message") <- c("Line 1 of Message",
                                 "Line 2 of Message")
xList <- xtableList(mtcarsList)
print.xtableList(xList)
print.xtableList(xList, colnames.format = "multiple")